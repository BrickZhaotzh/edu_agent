"""配置加载模块 — YAML + .env 统一配置管理"""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def load_env() -> None:
    """加载 .env 文件中的环境变量"""
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def load_yaml(filename: str) -> dict[str, Any]:
    """加载 config/ 目录下的 YAML 配置文件"""
    config_path = PROJECT_ROOT / "config" / filename
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class Settings:
    """全局配置单例"""

    _instance: "Settings | None" = None

    def __new__(cls) -> "Settings":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        load_env()
        self._settings = load_yaml("settings.yaml")
        self._registry = load_yaml("agent_registry.yaml")
        self._initialized = True

    # --- LLM 配置 ---
    @property
    def api_key(self) -> str:
        key = os.getenv("ZHIPUAI_API_KEY", "")
        if not key:
            raise ValueError("请设置 ZHIPUAI_API_KEY 环境变量")
        return key

    @property
    def model(self) -> str:
        return os.getenv("GLM_MODEL", self._settings["llm"]["model"])

    @property
    def temperature(self) -> float:
        return float(os.getenv("GLM_TEMPERATURE", self._settings["llm"]["temperature"]))

    @property
    def max_tokens(self) -> int:
        return int(os.getenv("GLM_MAX_TOKENS", self._settings["llm"]["max_tokens"]))

    @property
    def top_p(self) -> float:
        return self._settings["llm"].get("top_p", 0.9)

    @property
    def stream(self) -> bool:
        return self._settings["llm"].get("stream", True)

    # --- 知识库配置 ---
    @property
    def knowledge_config(self) -> dict:
        return self._settings.get("knowledge", {})

    # --- 文档导出配置 ---
    @property
    def document_config(self) -> dict:
        return self._settings.get("document", {})

    @property
    def output_dir(self) -> Path:
        d = PROJECT_ROOT / self._settings.get("document", {}).get("output_dir", "output")
        d.mkdir(parents=True, exist_ok=True)
        return d

    # --- 应用配置 ---
    @property
    def app_config(self) -> dict:
        return self._settings.get("app", {})

    # --- 云端知识库配置 ---
    @property
    def cloud_knowledge_config(self) -> dict:
        return self._settings.get("cloud_knowledge", {})

    @property
    def cloud_knowledge_enabled(self) -> bool:
        return self.cloud_knowledge_config.get("enabled", False)

    def get_cloud_kb_id(self, local_kb_id: str) -> str | None:
        """根据本地知识库标识获取对应的云端知识库ID"""
        mapping = self.cloud_knowledge_config.get("mapping", {})
        return mapping.get(local_kb_id)

    # --- Agent 注册表 ---
    @property
    def agent_registry(self) -> dict:
        return self._registry

    def get_agent_info(self, agent_id: str) -> dict | None:
        """根据 agent_id（如 A1.1）获取智能体注册信息"""
        for cat in self._registry.get("categories", {}).values():
            for agent in cat.get("agents", []):
                if agent["id"] == agent_id:
                    return agent
        return None

    def get_category_agents(self, category: str) -> list[dict]:
        """获取某类别下的所有智能体信息"""
        cat = self._registry.get("categories", {}).get(category, {})
        return cat.get("agents", [])


# 便捷访问
settings = Settings()
