"""Agent 抽象基类 — 所有智能体的统一接口"""

import json
import logging
from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Any

from pydantic import BaseModel

from src.core.cloud_knowledge import CloudKnowledgeManager
from src.core.config import settings
from src.core.document_gen import DocumentGenerator
from src.core.knowledge_base import KnowledgeBase
from src.core.llm_client import GLMClient
from src.core.models import AgentInput, AgentOutput
from src.core.prompt_engine import PromptEngine

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """智能体抽象基类

    子类需实现:
        - agent_id: 智能体ID（如 "A1.1"）
        - agent_name: 智能体名称
        - system_prompt_template: system提示词模板路径
        - user_prompt_template: user提示词模板路径
        - input_model: 输入模型类
        - output_model: 输出模型类
    """

    agent_id: str = ""
    agent_name: str = ""
    system_prompt_template: str = ""
    user_prompt_template: str = ""
    input_model: type[BaseModel] = AgentInput
    output_model: type[BaseModel] = AgentOutput

    def __init__(
        self,
        llm_client: GLMClient | None = None,
        prompt_engine: PromptEngine | None = None,
        knowledge_base: KnowledgeBase | None = None,
        doc_gen: DocumentGenerator | None = None,
    ):
        self.llm = llm_client or GLMClient()
        self.prompt = prompt_engine or PromptEngine()
        self.kb = knowledge_base or KnowledgeBase()
        self.doc = doc_gen or DocumentGenerator()
        # 云端知识库（仅在功能启用时初始化）
        self._cloud_kb: CloudKnowledgeManager | None = None
        if settings.cloud_knowledge_enabled:
            self._cloud_kb = CloudKnowledgeManager()

    def run(self, input_data: BaseModel) -> BaseModel:
        """同步执行：输入 → 构建上下文 → 组装提示词 → 调用LLM → 解析输出"""
        try:
            context = self._build_context(input_data)
            messages = self._build_messages(context)
            retrieval_tools = self._get_retrieval_tools(input_data)
            raw_output = self.llm.chat(
                messages, tools=retrieval_tools or None
            )
            return self._parse_output(raw_output, context)
        except Exception as e:
            logger.error(f"[{self.agent_id}] 执行失败: {e}")
            return self.output_model(
                agent_id=self.agent_id,
                agent_name=self.agent_name,
                content="",
                success=False,
                error_message=str(e),
            )

    def run_stream(self, input_data: BaseModel) -> Generator[str, None, None]:
        """流式执行：逐块返回文本"""
        try:
            context = self._build_context(input_data)
            messages = self._build_messages(context)
            retrieval_tools = self._get_retrieval_tools(input_data)
            yield from self.llm.chat_stream(
                messages, tools=retrieval_tools or None
            )
        except Exception as e:
            logger.error(f"[{self.agent_id}] 流式执行失败: {e}")
            yield f"\n\n[错误] {e}"

    def run_and_collect_stream(self, input_data: BaseModel) -> BaseModel:
        """流式执行但收集完整输出，返回结构化结果"""
        parts = []
        for chunk in self.run_stream(input_data):
            parts.append(chunk)
        full_text = "".join(parts)
        context = self._build_context(input_data)
        return self._parse_output(full_text, context)

    def _get_retrieval_tools(self, input_data: BaseModel) -> list[dict]:
        """收集当前 agent 需要的 retrieval tools

        来源：
        1. agent_registry 中本 agent 的 knowledge 字段
        2. input_data 中的 knowledge_ids 字段
        """
        if not self._cloud_kb:
            return []

        kb_ids: list[str] = []

        # 从注册表获取
        agent_info = settings.get_agent_info(self.agent_id)
        if agent_info:
            kb_ids.extend(agent_info.get("knowledge", []))

        # 从输入数据获取
        data = input_data.model_dump()
        kb_ids.extend(data.get("knowledge_ids", []))

        # 去重
        kb_ids = list(dict.fromkeys(kb_ids))
        return self._cloud_kb.build_retrieval_tools(kb_ids)

    def _build_context(self, input_data: BaseModel) -> dict[str, Any]:
        """构建上下文：合并输入数据 + 知识库检索结果

        子类可覆写以添加特定逻辑。
        """
        data = input_data.model_dump()
        context: dict[str, Any] = {"input": data}

        # 如果输入指定了知识库，加载并检索
        knowledge_ids = data.get("knowledge_ids", [])
        query = data.get("query", "")
        kb_texts = {}
        for kb_id in knowledge_ids:
            self.kb.load(kb_id)
            kb_texts[kb_id] = self.kb.get_context_text(kb_id, query)
        if kb_texts:
            context["knowledge"] = kb_texts

        # 上游管线数据
        if data.get("upstream_output"):
            context["upstream"] = data["upstream_output"]

        # 用户上传附件
        if data.get("file_content"):
            context["uploaded_file"] = {
                "name": data.get("file_name", ""),
                "content": data["file_content"],
            }

        return context

    def _build_messages(self, context: dict[str, Any]) -> list[dict[str, str]]:
        """组装 LLM 消息列表

        优先使用 Jinja2 模板；如模板未配置，使用默认提示词。
        """
        if self.system_prompt_template and self.user_prompt_template:
            return self.prompt.build_messages(
                self.system_prompt_template,
                self.user_prompt_template,
                system_vars=context,
                user_vars=context,
            )

        # 回退：使用默认提示词
        system_prompt = self._default_system_prompt()
        user_prompt = self._format_user_prompt(context)
        return self.prompt.build_messages_from_strings(system_prompt, user_prompt)

    def _default_system_prompt(self) -> str:
        """默认 system 提示词，子类应覆写"""
        return (
            f"你是「{self.agent_name}」智能助手（ID: {self.agent_id}），"
            f"专注于K-12科创教育领域。请用简体中文回答，输出使用Markdown格式。"
        )

    @abstractmethod
    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        """格式化 user 提示词（当不使用Jinja2模板时）

        子类必须实现此方法。
        """
        ...

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> BaseModel:
        """将 LLM 原始输出解析为结构化输出模型

        默认实现将原始文本放入 content 字段。子类可覆写以提取结构化数据。
        """
        return self.output_model(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )

    def export_markdown(self, output: BaseModel, filename: str | None = None) -> str:
        """导出输出为 Markdown 文件"""
        fn = filename or f"{self.agent_id}_{self.agent_name}.md"
        data = output.model_dump()
        path = self.doc.save_markdown(data.get("content", ""), fn)
        return str(path)

    def export_word(self, output: BaseModel, filename: str | None = None) -> str:
        """导出输出为 Word 文件"""
        fn = filename or f"{self.agent_id}_{self.agent_name}.docx"
        data = output.model_dump()
        path = self.doc.save_word(data.get("content", ""), fn, title=self.agent_name)
        return str(path)


def run_agent_cli(agent_class: type["BaseAgent"], input_model: type[BaseModel]) -> None:
    """CLI 入口辅助函数，供 Skill 调用 `python3 -m src.agents.xxx` 时使用"""
    import sys

    if len(sys.argv) < 2:
        print(f"用法: python3 -m {agent_class.__module__} '<JSON输入>'", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[1]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # 如果不是 JSON，当作 query 字符串
        data = {"query": raw}

    input_data = input_model(**data)
    agent = agent_class()
    result = agent.run(input_data)
    print(result.model_dump_json(indent=2))
