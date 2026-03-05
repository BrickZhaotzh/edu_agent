"""对话持久化 — JSON 文件存储"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from src.core.config import PROJECT_ROOT

logger = logging.getLogger(__name__)


class ChatStorage:
    """对话记录 JSON 持久化管理"""

    def __init__(self, base_dir: str | None = None) -> None:
        if base_dir:
            self._base = Path(base_dir)
        else:
            self._base = PROJECT_ROOT / "data" / "conversations"
        self._base.mkdir(parents=True, exist_ok=True)

    def _agent_dir(self, agent_id: str) -> Path:
        d = self._base / agent_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    @staticmethod
    def generate_id() -> str:
        return f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    @staticmethod
    def generate_title(first_user_message: str, max_len: int = 20) -> str:
        text = first_user_message
        # 去掉附件标记 "📎 **filename**\n\n..."
        if text.startswith("📎"):
            lines = text.split("\n", 2)
            text = lines[-1] if len(lines) > 1 else text
        text = text.strip()
        if len(text) > max_len:
            text = text[:max_len] + "..."
        return text or "新对话"

    def save(self, agent_id: str, conversation: dict[str, Any]) -> Path:
        conversation["updated_at"] = datetime.now().isoformat()
        path = self._agent_dir(agent_id) / f"{conversation['id']}.json"
        path.write_text(
            json.dumps(conversation, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    def load(self, agent_id: str, conv_id: str) -> dict[str, Any] | None:
        path = self._agent_dir(agent_id) / f"{conv_id}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def list_conversations(self, agent_id: str) -> list[dict[str, Any]]:
        d = self._base / agent_id
        if not d.exists():
            return []
        convos = []
        for path in d.glob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                convos.append({
                    "id": data["id"],
                    "title": data.get("title", "未命名"),
                    "updated_at": data.get("updated_at", ""),
                    "message_count": len(data.get("messages", [])),
                })
            except Exception as e:
                logger.warning(f"[ChatStorage] 读取失败 {path}: {e}")
        convos.sort(key=lambda x: x["updated_at"], reverse=True)
        return convos

    def delete(self, agent_id: str, conv_id: str) -> bool:
        path = self._agent_dir(agent_id) / f"{conv_id}.json"
        if path.exists():
            path.unlink()
            return True
        return False

    def count(self, agent_id: str) -> int:
        d = self._base / agent_id
        if not d.exists():
            return 0
        return len(list(d.glob("*.json")))

    def count_all(self) -> dict[str, int]:
        counts = {}
        if not self._base.exists():
            return counts
        for d in self._base.iterdir():
            if d.is_dir():
                n = len(list(d.glob("*.json")))
                if n > 0:
                    counts[d.name] = n
        return counts
