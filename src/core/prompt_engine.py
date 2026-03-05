"""Jinja2 提示词模板引擎 — 加载、渲染、组合"""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import PROJECT_ROOT

PROMPTS_DIR = PROJECT_ROOT / "src" / "prompts"


class PromptEngine:
    """提示词模板管理器"""

    def __init__(self, prompts_dir: Path | None = None):
        self._dir = prompts_dir or PROMPTS_DIR
        self._env = Environment(
            loader=FileSystemLoader(str(self._dir)),
            autoescape=select_autoescape([]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_path: str, **kwargs: Any) -> str:
        """渲染指定模板

        Args:
            template_path: 模板相对路径，如 "category_a/policy_insight.j2"
            **kwargs: 模板变量
        """
        template = self._env.get_template(template_path)
        return template.render(**kwargs)

    def build_messages(
        self,
        system_template: str,
        user_template: str,
        system_vars: dict[str, Any] | None = None,
        user_vars: dict[str, Any] | None = None,
    ) -> list[dict[str, str]]:
        """构建 system + user 两条消息

        Args:
            system_template: system 提示词模板路径
            user_template: user 提示词模板路径
            system_vars: system 模板变量
            user_vars: user 模板变量
        """
        return [
            {"role": "system", "content": self.render(system_template, **(system_vars or {}))},
            {"role": "user", "content": self.render(user_template, **(user_vars or {}))},
        ]

    def build_messages_from_strings(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> list[dict[str, str]]:
        """从纯字符串构建消息（不使用模板文件）"""
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
