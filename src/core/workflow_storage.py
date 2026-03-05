"""工作流持久化 — JSON 文件存储"""

import json
import logging
from pathlib import Path
from typing import Any

from src.core.config import PROJECT_ROOT, settings
from src.core.workflow_models import WorkflowDefinition

logger = logging.getLogger(__name__)


class WorkflowStorage:
    """工作流 JSON 持久化管理"""

    def __init__(self, storage_dir: str | None = None) -> None:
        if storage_dir:
            self._dir = Path(storage_dir)
        else:
            cfg = settings._settings.get("workflow", {})
            rel = cfg.get("storage_dir", "output/workflows")
            self._dir = PROJECT_ROOT / rel
        self._dir.mkdir(parents=True, exist_ok=True)

    def save(self, workflow: WorkflowDefinition) -> Path:
        """保存工作流到 JSON 文件"""
        path = self._dir / f"{workflow.id}.json"
        data = workflow.model_dump(mode="json")
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"[WorkflowStorage] 已保存: {path}")
        return path

    def load(self, workflow_id: str) -> WorkflowDefinition | None:
        """加载指定 ID 的工作流"""
        path = self._dir / f"{workflow_id}.json"
        if not path.exists():
            logger.warning(f"[WorkflowStorage] 文件不存在: {path}")
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return WorkflowDefinition.model_validate(data)

    def list_all(self) -> list[dict[str, Any]]:
        """列出所有已保存的工作流（返回摘要信息）"""
        workflows = []
        for path in sorted(self._dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                workflows.append({
                    "id": data.get("id", path.stem),
                    "name": data.get("name", "未命名"),
                    "description": data.get("description", ""),
                    "node_count": len(data.get("nodes", [])),
                    "updated_at": data.get("updated_at", ""),
                })
            except Exception as e:
                logger.warning(f"[WorkflowStorage] 读取失败 {path}: {e}")
        return workflows

    def delete(self, workflow_id: str) -> bool:
        """删除指定工作流"""
        path = self._dir / f"{workflow_id}.json"
        if path.exists():
            path.unlink()
            logger.info(f"[WorkflowStorage] 已删除: {path}")
            return True
        return False
