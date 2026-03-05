"""云端知识库管理 — 智谱AI retrieval 工具集成"""

import logging
from pathlib import Path
from typing import Any

from zhipuai import ZhipuAI

from .config import settings

logger = logging.getLogger(__name__)


class CloudKnowledgeManager:
    """云端知识库管理器

    封装智谱AI知识库 API，提供：
    - 知识库 CRUD
    - 文档上传/管理
    - retrieval tool 构建（供 LLM 调用时自动 RAG）
    """

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key or settings.api_key
        self._client = ZhipuAI(api_key=self._api_key)

    # ========== 知识库 CRUD ==========

    def create_knowledge_base(
        self,
        name: str,
        description: str = "",
        embedding_id: int = 3,
    ) -> dict[str, Any]:
        """创建云端知识库

        Args:
            name: 知识库名称
            description: 知识库描述
            embedding_id: 向量化模型ID（3=embedding-3）

        Returns:
            API 返回的知识库信息，包含 id 字段
        """
        result = self._client.knowledge.create(
            embedding_id=embedding_id,
            name=name,
            description=description,
        )
        logger.info(f"创建知识库: {name} -> {result.id}")
        return {"id": result.id, "name": name, "description": description}

    def list_knowledge_bases(self, page: int = 1, size: int = 10) -> list[dict[str, Any]]:
        """列出所有云端知识库"""
        result = self._client.knowledge.query(page=page, size=size)
        return [
            {
                "id": kb.id,
                "name": kb.name,
                "description": kb.description or "",
                "embedding_id": kb.embedding_id,
            }
            for kb in result.list
        ]

    def delete_knowledge_base(self, kb_id: str) -> bool:
        """删除云端知识库"""
        try:
            self._client.knowledge.delete(knowledge_id=kb_id)
            logger.info(f"删除知识库: {kb_id}")
            return True
        except Exception as e:
            logger.error(f"删除知识库失败: {kb_id}, {e}")
            return False

    # ========== 文档管理 ==========

    def upload_document(
        self,
        kb_id: str,
        file_path: str | Path,
        custom_separator: list[str] | None = None,
        sentence_size: int = 300,
    ) -> dict[str, Any]:
        """上传文档到云端知识库

        支持格式: doc/docx/pdf/xlsx/txt/md，单文件 ≤ 50MB

        Args:
            kb_id: 知识库ID
            file_path: 文件路径
            custom_separator: 自定义分段符
            sentence_size: 分段长度

        Returns:
            包含 document_id 和 filename 的字典
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        result = self._client.knowledge.document.create(
            file=open(file_path, "rb"),
            purpose="retrieval",
            knowledge_id=kb_id,
            custom_separator=custom_separator or ["\n\n"],
            sentence_size=sentence_size,
        )
        # result.successInfos 包含成功上传的文档信息
        doc_id = ""
        if result.successInfos:
            doc_id = result.successInfos[0].documentId
        logger.info(f"上传文档: {file_path.name} -> kb={kb_id}, doc={doc_id}")
        return {
            "document_id": doc_id,
            "filename": file_path.name,
        }

    def list_documents(self, kb_id: str, page: int = 1, limit: int = 20) -> list[dict[str, Any]]:
        """列出知识库中的文档"""
        result = self._client.knowledge.document.list(
            knowledge_id=kb_id,
            purpose="retrieval",
            page=str(page),
            limit=str(limit),
        )
        return [
            {
                "id": doc.id,
                "name": doc.name,
                "word_num": doc.word_num,
                "embedding_stat": doc.embedding_stat,
            }
            for doc in result.list
        ]

    def delete_document(self, document_id: str) -> bool:
        """删除知识库中的文档"""
        try:
            self._client.knowledge.document.delete(document_id=document_id)
            logger.info(f"删除文档: {document_id}")
            return True
        except Exception as e:
            logger.error(f"删除文档失败: {document_id}, {e}")
            return False

    # ========== Retrieval Tool 构建 ==========

    def build_retrieval_tool(self, local_kb_id: str) -> dict[str, Any] | None:
        """根据本地 kb_id 构建 retrieval tool dict

        查找 mapping 中对应的云端 kb_id，生成智谱 retrieval 工具配置。

        Returns:
            retrieval tool dict，或 None（无映射时）
        """
        cloud_kb_id = settings.get_cloud_kb_id(local_kb_id)
        if not cloud_kb_id:
            return None

        config = settings.cloud_knowledge_config
        prompt_template = config.get(
            "prompt_template",
            "从文档:\n{{knowledge}}\n回答:\n{{question}}",
        )

        return {
            "type": "retrieval",
            "retrieval": {
                "knowledge_id": cloud_kb_id,
                "prompt_template": prompt_template,
            },
        }

    def build_retrieval_tools(self, kb_ids: list[str]) -> list[dict[str, Any]]:
        """批量构建 retrieval tools

        Args:
            kb_ids: 本地知识库标识列表

        Returns:
            非空 retrieval tool 列表
        """
        tools = []
        for kb_id in kb_ids:
            tool = self.build_retrieval_tool(kb_id)
            if tool:
                tools.append(tool)
        return tools
