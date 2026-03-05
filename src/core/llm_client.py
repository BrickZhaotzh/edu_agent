"""GLM-4.7 客户端封装 — 同步/流式/工具调用"""

from collections.abc import Generator
from typing import Any

from zhipuai import ZhipuAI

from .config import settings


class GLMClient:
    """GLM-4.7 大模型客户端"""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ):
        self._api_key = api_key or settings.api_key
        self._model = model or settings.model
        self._client = ZhipuAI(api_key=self._api_key)

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        tools: list[dict] | None = None,
    ) -> str:
        """同步调用，返回完整文本

        GLM-4.7 是推理模型，输出分为 reasoning_content（思考过程）和 content（最终回答）。
        优先返回 content，若为空则回退到 reasoning_content。
        """
        params = self._build_params(messages, temperature, max_tokens, top_p, tools)
        response = self._client.chat.completions.create(**params)
        msg = response.choices[0].message
        content = msg.content or ""
        if not content and hasattr(msg, "reasoning_content") and msg.reasoning_content:
            content = msg.reasoning_content
        return content

    def chat_stream(
        self,
        messages: list[dict[str, str]],
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        tools: list[dict] | None = None,
    ) -> Generator[str, None, None]:
        """流式调用，逐块返回文本

        GLM-4.7 推理模型流式输出：先产出 reasoning_content，再产出 content。
        仅返回 content 部分；如果全程无 content 则回退返回 reasoning_content。
        """
        params = self._build_params(messages, temperature, max_tokens, top_p, tools)
        params["stream"] = True
        response = self._client.chat.completions.create(**params)
        has_content = False
        reasoning_parts = []
        for chunk in response:
            if chunk.choices:
                delta = chunk.choices[0].delta
                if delta.content:
                    has_content = True
                    yield delta.content
                elif not has_content and hasattr(delta, "reasoning_content") and delta.reasoning_content:
                    reasoning_parts.append(delta.reasoning_content)
        # 回退：如果没有 content 输出，返回推理过程
        if not has_content and reasoning_parts:
            yield "".join(reasoning_parts)

    def chat_with_tools(
        self,
        messages: list[dict[str, str]],
        tools: list[dict],
        temperature: float | None = None,
    ) -> dict[str, Any]:
        """带工具调用的对话，返回完整 response 供调用方处理"""
        params = self._build_params(messages, temperature, tools=tools)
        response = self._client.chat.completions.create(**params)
        choice = response.choices[0]
        result: dict[str, Any] = {"content": choice.message.content or ""}
        if choice.message.tool_calls:
            result["tool_calls"] = [
                {
                    "id": tc.id,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in choice.message.tool_calls
            ]
        return result

    def _build_params(
        self,
        messages: list[dict[str, str]],
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        tools: list[dict] | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "temperature": temperature if temperature is not None else settings.temperature,
            "max_tokens": max_tokens if max_tokens is not None else settings.max_tokens,
            "top_p": top_p if top_p is not None else settings.top_p,
        }
        if tools:
            params["tools"] = tools
        return params
