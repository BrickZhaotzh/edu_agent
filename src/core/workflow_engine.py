"""工作流执行引擎 — 拓扑排序 + DAG 顺序执行 + 流式输出"""

import importlib
import logging
from collections import deque
from collections.abc import Callable, Generator
from typing import Any

from src.core.config import settings
from src.core.models import AgentInput
from src.core.workflow_models import NodeStatus, WorkflowDefinition, WorkflowNode

logger = logging.getLogger(__name__)


class WorkflowError(Exception):
    """工作流执行错误"""


class WorkflowEngine:
    """DAG 工作流执行引擎

    职责：
    1. 校验工作流定义（agent_id 合法、边合法、无环）
    2. 拓扑排序生成执行顺序
    3. 按顺序执行各节点，自动传递 upstream_output
    4. 错误隔离：上游失败 → 下游 skipped
    """

    def __init__(self) -> None:
        self._agent_cache: dict[str, Any] = {}

    # ── 校验 ──

    def validate(self, workflow: WorkflowDefinition) -> list[str]:
        """校验工作流定义，返回错误列表（空列表表示合法）"""
        errors: list[str] = []
        node_ids = {n.id for n in workflow.nodes}

        # 检查 agent_id 是否存在于注册表
        for node in workflow.nodes:
            info = settings.get_agent_info(node.agent_id)
            if info is None:
                errors.append(f"节点 {node.id}: agent_id '{node.agent_id}' 不在注册表中")

        # 检查边的端点是否合法
        for edge in workflow.edges:
            if edge.source not in node_ids:
                errors.append(f"边 {edge.id}: 源节点 '{edge.source}' 不存在")
            if edge.target not in node_ids:
                errors.append(f"边 {edge.id}: 目标节点 '{edge.target}' 不存在")

        # 检查是否有环（尝试拓扑排序）
        try:
            self.topological_sort(workflow)
        except WorkflowError as e:
            errors.append(str(e))

        return errors

    # ── 拓扑排序 ──

    def topological_sort(self, workflow: WorkflowDefinition) -> list[str]:
        """Kahn 算法拓扑排序，返回节点 ID 执行顺序

        Raises:
            WorkflowError: 存在环路
        """
        if not workflow.nodes:
            return []

        # 构建邻接表和入度表
        in_degree: dict[str, int] = {n.id: 0 for n in workflow.nodes}
        adjacency: dict[str, list[str]] = {n.id: [] for n in workflow.nodes}

        for edge in workflow.edges:
            if edge.source in adjacency and edge.target in in_degree:
                adjacency[edge.source].append(edge.target)
                in_degree[edge.target] += 1

        # 入度为 0 的节点入队
        queue: deque[str] = deque()
        for nid, deg in in_degree.items():
            if deg == 0:
                queue.append(nid)

        order: list[str] = []
        while queue:
            nid = queue.popleft()
            order.append(nid)
            for neighbor in adjacency[nid]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(workflow.nodes):
            raise WorkflowError("工作流存在环路，无法执行")

        return order

    # ── 执行 ──

    def execute(
        self,
        workflow: WorkflowDefinition,
        query: str,
        on_node_start: Callable[[str], None] | None = None,
        on_node_complete: Callable[[str, dict], None] | None = None,
        on_node_error: Callable[[str, str], None] | None = None,
    ) -> dict[str, dict[str, Any]]:
        """同步顺序执行整个工作流

        Args:
            workflow: 工作流定义
            query: 全局 query
            on_node_start: 节点开始回调
            on_node_complete: 节点完成回调（node_id, output_dict）
            on_node_error: 节点失败回调（node_id, error_msg）

        Returns:
            {node_id: {"content": ..., "structured_data": ..., ...}}
        """
        order = self.topological_sort(workflow)
        results: dict[str, dict[str, Any]] = {}

        for node_id in order:
            node = workflow.get_node(node_id)
            if node is None:
                continue

            # 检查上游是否有失败/跳过
            upstream_nodes = workflow.get_upstream_nodes(node_id)
            if any(n.status in (NodeStatus.FAILED, NodeStatus.SKIPPED) for n in upstream_nodes):
                node.status = NodeStatus.SKIPPED
                logger.info(f"[Workflow] 跳过节点 {node_id}（上游失败）")
                continue

            # 执行
            node.status = NodeStatus.RUNNING
            if on_node_start:
                on_node_start(node_id)

            try:
                output = self._execute_node(workflow, node, query, results)
                node.status = NodeStatus.COMPLETED
                node.output = output
                results[node_id] = output
                if on_node_complete:
                    on_node_complete(node_id, output)
            except Exception as e:
                node.status = NodeStatus.FAILED
                node.output = {"error": str(e)}
                results[node_id] = {"error": str(e)}
                logger.error(f"[Workflow] 节点 {node_id} 执行失败: {e}")
                if on_node_error:
                    on_node_error(node_id, str(e))

        return results

    def execute_node_stream(
        self,
        workflow: WorkflowDefinition,
        node_id: str,
        query: str,
        results: dict[str, dict[str, Any]],
    ) -> Generator[str, None, None]:
        """流式执行单个节点，逐块 yield 文本

        Args:
            workflow: 工作流定义
            node_id: 要执行的节点 ID
            query: 全局 query
            results: 已有节点的执行结果
        """
        node = workflow.get_node(node_id)
        if node is None:
            yield f"[错误] 节点 {node_id} 不存在"
            return

        # 检查上游
        upstream_nodes = workflow.get_upstream_nodes(node_id)
        if any(n.status in (NodeStatus.FAILED, NodeStatus.SKIPPED) for n in upstream_nodes):
            node.status = NodeStatus.SKIPPED
            yield f"[跳过] 上游节点失败，跳过 {node.agent_id}"
            return

        node.status = NodeStatus.RUNNING
        try:
            agent = self._get_agent(node.agent_id)
            input_data = self._build_input(agent, node, query, upstream_nodes, results)
            full_text = ""
            for chunk in agent.run_stream(input_data):
                full_text += chunk
                yield chunk

            node.status = NodeStatus.COMPLETED
            node.output = {"content": full_text, "agent_id": node.agent_id}
            results[node_id] = node.output
        except Exception as e:
            node.status = NodeStatus.FAILED
            error_msg = f"[错误] {node.agent_id} 执行失败: {e}"
            node.output = {"error": str(e)}
            results[node_id] = node.output
            logger.error(f"[Workflow] 节点 {node_id} 流式执行失败: {e}")
            yield error_msg

    # ── 内部方法 ──

    def _execute_node(
        self,
        workflow: WorkflowDefinition,
        node: WorkflowNode,
        query: str,
        results: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        """同步执行单个节点，返回输出字典"""
        agent = self._get_agent(node.agent_id)
        upstream_nodes = workflow.get_upstream_nodes(node.id)
        input_data = self._build_input(agent, node, query, upstream_nodes, results)
        output = agent.run(input_data)
        return output.model_dump()

    def _get_agent(self, agent_id: str) -> Any:
        """动态实例化 Agent，带缓存"""
        if agent_id in self._agent_cache:
            return self._agent_cache[agent_id]

        info = settings.get_agent_info(agent_id)
        if info is None:
            raise WorkflowError(f"Agent '{agent_id}' 未在注册表中找到")

        module_path = info["module"]
        class_name = info["class"]

        try:
            module = importlib.import_module(module_path)
            agent_class = getattr(module, class_name)
            agent = agent_class()
        except Exception as e:
            raise WorkflowError(f"实例化 Agent '{agent_id}' 失败: {e}") from e

        self._agent_cache[agent_id] = agent
        return agent

    def _build_input(
        self,
        agent: Any,
        node: WorkflowNode,
        query: str,
        upstream_nodes: list[WorkflowNode],
        results: dict[str, dict[str, Any]],
    ) -> Any:
        """构建 Agent 输入对象

        - query: 全局 query
        - knowledge_ids: 节点配置的知识库
        - upstream_output: 上游输出（单上游直传，多上游合并）
        - custom_params: 节点自定义参数
        """
        params: dict[str, Any] = {"query": query}

        # 知识库
        if node.knowledge_ids:
            params["knowledge_ids"] = node.knowledge_ids

        # 上游输出
        upstream_output = self._merge_upstream(upstream_nodes, results)
        if upstream_output:
            params["upstream_output"] = upstream_output

        # 自定义参数
        if node.custom_params:
            params.update(node.custom_params)

        # 构建输入模型（优先使用 Agent 的 input_model，字段不匹配时回退到 AgentInput）
        try:
            return agent.input_model(**params)
        except Exception:
            # 回退：只传基础字段
            base_params = {
                "query": query,
                "knowledge_ids": params.get("knowledge_ids", []),
                "upstream_output": upstream_output,
            }
            return AgentInput(**base_params)

    def _merge_upstream(
        self,
        upstream_nodes: list[WorkflowNode],
        results: dict[str, dict[str, Any]],
    ) -> dict[str, Any] | None:
        """合并上游节点输出

        - 无上游 → None
        - 单上游 → 直接返回该输出
        - 多上游 → {agent_id: output, ...}
        """
        completed = [
            (n.agent_id, results[n.id])
            for n in upstream_nodes
            if n.id in results and n.status == NodeStatus.COMPLETED
        ]
        if not completed:
            return None
        if len(completed) == 1:
            return completed[0][1]
        return {aid: out for aid, out in completed}
