"""工作流数据模型 — 可视化编排器的核心数据结构"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class NodeStatus(str, Enum):
    """工作流节点执行状态"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowNode(BaseModel):
    """工作流节点 — 对应一个 Agent"""

    id: str = Field(..., description="节点唯一标识，如 node_abc123")
    agent_id: str = Field(..., description="Agent 注册 ID，如 A1.1")
    label: str = Field(default="", description="节点显示名称")
    position: tuple[float, float] = Field(default=(0, 0), description="画布坐标 (x, y)")
    knowledge_ids: list[str] = Field(default_factory=list, description="该节点配置的知识库 ID")
    reference_urls: list[str] = Field(default_factory=list, description="参考资料 URL 列表")
    custom_params: dict[str, Any] = Field(default_factory=dict, description="Agent 特有参数")
    status: NodeStatus = Field(default=NodeStatus.PENDING, description="执行状态")
    output: dict[str, Any] | None = Field(default=None, description="执行输出")


class WorkflowEdge(BaseModel):
    """工作流边 — 连接两个节点"""

    id: str = Field(..., description="边唯一标识")
    source: str = Field(..., description="源节点 ID")
    target: str = Field(..., description="目标节点 ID")


class WorkflowDefinition(BaseModel):
    """工作流定义 — 包含节点、边和全局配置"""

    id: str = Field(..., description="工作流唯一标识")
    name: str = Field(..., description="工作流名称")
    description: str = Field(default="", description="工作流描述")
    nodes: list[WorkflowNode] = Field(default_factory=list)
    edges: list[WorkflowEdge] = Field(default_factory=list)
    global_query: str = Field(default="", description="全局输入 query")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def get_node(self, node_id: str) -> WorkflowNode | None:
        """根据 ID 获取节点"""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def get_upstream_nodes(self, node_id: str) -> list[WorkflowNode]:
        """获取某节点的所有上游节点"""
        upstream_ids = [e.source for e in self.edges if e.target == node_id]
        return [n for n in self.nodes if n.id in upstream_ids]

    def get_downstream_nodes(self, node_id: str) -> list[WorkflowNode]:
        """获取某节点的所有下游节点"""
        downstream_ids = [e.target for e in self.edges if e.source == node_id]
        return [n for n in self.nodes if n.id in downstream_ids]

    def get_root_nodes(self) -> list[WorkflowNode]:
        """获取所有入度为 0 的根节点"""
        target_ids = {e.target for e in self.edges}
        return [n for n in self.nodes if n.id not in target_ids]
