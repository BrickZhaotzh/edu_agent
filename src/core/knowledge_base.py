"""本地知识库加载与检索 — 基于 Markdown 文件的轻量检索"""

import re
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT, settings


class KnowledgeBase:
    """本地知识库管理器

    加载指定目录下的 .md/.txt 文件，支持关键词检索和分块读取。
    """

    def __init__(self):
        self._documents: dict[str, list[dict[str, Any]]] = {}
        self._kb_config = settings.knowledge_config

    def load(self, kb_id: str, directory: Path | None = None) -> int:
        """加载知识库

        Args:
            kb_id: 知识库标识（如 "policies", "competitor_reports"）
            directory: 知识库目录路径，None 则从配置读取

        Returns:
            加载的文档数量
        """
        # 云端知识库启用且有映射时，跳过本地加载（由 retrieval tool 接管）
        if settings.cloud_knowledge_enabled and settings.get_cloud_kb_id(kb_id):
            self._documents[kb_id] = []
            return 0

        if directory is None:
            dir_key = f"{kb_id}_dir"
            rel_path = self._kb_config.get(dir_key, f"src/knowledge/{kb_id}")
            directory = PROJECT_ROOT / rel_path

        if not directory.exists():
            return 0

        docs = []
        for file_path in sorted(directory.rglob("*.md")):
            text = file_path.read_text(encoding="utf-8")
            chunks = self._split_chunks(text, file_path.name)
            docs.extend(chunks)

        for file_path in sorted(directory.rglob("*.txt")):
            text = file_path.read_text(encoding="utf-8")
            chunks = self._split_chunks(text, file_path.name)
            docs.extend(chunks)

        self._documents[kb_id] = docs
        return len(docs)

    def search(self, kb_id: str, query: str, top_k: int | None = None) -> list[dict[str, Any]]:
        """关键词检索

        Args:
            kb_id: 知识库标识
            query: 检索关键词（空格分隔多个关键词，取并集）
            top_k: 返回结果数量上限

        Returns:
            匹配的文档块列表，按相关度排序
        """
        top_k = top_k or self._kb_config.get("top_k", 5)
        docs = self._documents.get(kb_id, [])
        if not docs or not query.strip():
            return docs[:top_k]

        keywords = [kw.lower() for kw in query.strip().split() if kw]
        scored = []
        for doc in docs:
            text_lower = doc["content"].lower()
            score = sum(text_lower.count(kw) for kw in keywords)
            if score > 0:
                scored.append((score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]

    def get_context_text(self, kb_id: str, query: str, top_k: int | None = None) -> str:
        """检索并拼接为上下文字符串，直接注入到提示词中"""
        results = self.search(kb_id, query, top_k)
        if not results:
            return ""
        parts = []
        for i, doc in enumerate(results, 1):
            parts.append(f"--- 参考文档 {i}: {doc['source']} ---\n{doc['content']}")
        return "\n\n".join(parts)

    def list_loaded(self) -> dict[str, int]:
        """返回已加载的知识库及其文档块数量"""
        return {kb_id: len(docs) for kb_id, docs in self._documents.items()}

    def _split_chunks(self, text: str, source: str) -> list[dict[str, Any]]:
        """按标题或固定长度分块"""
        chunk_size = self._kb_config.get("chunk_size", 2000)

        # 尝试按 Markdown 二级标题分块
        sections = re.split(r'\n(?=## )', text)
        chunks = []
        for section in sections:
            section = section.strip()
            if not section:
                continue
            if len(section) <= chunk_size:
                chunks.append({"source": source, "content": section})
            else:
                # 超长段落按固定长度切割
                for i in range(0, len(section), chunk_size):
                    piece = section[i:i + chunk_size]
                    if piece.strip():
                        chunks.append({"source": source, "content": piece})
        return chunks if chunks else [{"source": source, "content": text[:chunk_size]}]
