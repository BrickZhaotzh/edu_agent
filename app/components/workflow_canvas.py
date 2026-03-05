"""工作流画布组件 — 封装 streamlit-flow-component 交互"""

import sys
import uuid
from pathlib import Path
from typing import Any

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowEdge, StreamlitFlowNode
from streamlit_flow.layouts import ManualLayout
from streamlit_flow.state import StreamlitFlowState

from src.core.config import settings
from src.core.workflow_models import (
    NodeStatus,
    WorkflowDefinition,
    WorkflowEdge,
    WorkflowNode,
)

# ── 视觉常量 ──

_CAT_COLORS = {
    "A": ("#e3f2fd", "#1565c0"), "B": ("#f3e5f5", "#7b1fa2"),
    "C": ("#e8f5e9", "#2e7d32"), "D": ("#fff3e0", "#e65100"),
    "E": ("#fce4ec", "#c62828"), "F": ("#e0f2f1", "#00695c"),
}
_STATUS_STYLE = {
    NodeStatus.PENDING:   (None, None),
    NodeStatus.RUNNING:   ("#fff8e1", "#ffa000"),
    NodeStatus.COMPLETED: ("#e8f5e9", "#43a047"),
    NodeStatus.FAILED:    ("#ffebee", "#e53935"),
    NodeStatus.SKIPPED:   ("#eceff1", "#90a4ae"),
}
_STATUS_ICON = {
    NodeStatus.PENDING: "", NodeStatus.RUNNING: "⏳",
    NodeStatus.COMPLETED: "✅", NodeStatus.FAILED: "❌", NodeStatus.SKIPPED: "⏭️",
}


def short_id() -> str:
    return uuid.uuid4().hex[:8]


def get_agent_label(agent_id: str) -> str:
    info = settings.get_agent_info(agent_id)
    return f"{agent_id} {info['name']}" if info else agent_id


# ── 节点样式 ──

def _node_style(agent_id: str, status: str) -> dict:
    cat = agent_id[0].upper() if agent_id else "A"
    bg, border = _STATUS_STYLE.get(status, (None, None))
    if bg is None:
        bg, border = _CAT_COLORS.get(cat, ("#f5f5f5", "#bdbdbd"))
    return {
        "backgroundColor": bg,
        "border": f"2px solid {border}",
        "borderRadius": "6px",
        "padding": "4px 10px",
        "fontSize": "12px",
        "lineHeight": "1.3",
    }


def _node_content(node: WorkflowNode) -> str:
    icon = _STATUS_ICON.get(node.status, "")
    info = settings.get_agent_info(node.agent_id)
    name = info["name"] if info else node.agent_id
    prefix = f"{icon} " if icon else ""
    return f"{prefix}{node.agent_id} {name}"


# ── 位置计算 ──

def _calc_new_position(workflow: WorkflowDefinition) -> tuple[float, float]:
    """为新节点计算合理位置（在现有节点下方居中）"""
    if not workflow.nodes:
        return (250.0, 50.0)

    # 读取现有节点的实际位置（优先从画布状态读取）
    positions = []
    state_key = f"wf_state_{workflow.id}"
    if state_key in st.session_state:
        for n in st.session_state[state_key].nodes:
            p = n.position
            if isinstance(p, dict):
                positions.append((p["x"], p["y"]))
            else:
                positions.append(p)
    if not positions:
        positions = [n.position for n in workflow.nodes]

    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    center_x = sum(xs) / len(xs)
    max_y = max(ys)
    return (center_x, max_y + 100)


# ── 指纹 ──

def _fingerprint(workflow: WorkflowDefinition) -> str:
    parts = [f"{n.id}:{n.agent_id}:{n.status}" for n in workflow.nodes]
    parts += [f"{e.id}:{e.source}:{e.target}" for e in workflow.edges]
    return "|".join(parts)


# ══════════════════════════════════════
# 画布渲染（始终 ManualLayout，不触发组件重绘）
# ══════════════════════════════════════

def render_workflow_canvas(workflow: WorkflowDefinition) -> WorkflowDefinition:
    state_key = f"wf_state_{workflow.id}"
    fp_key = f"{state_key}_fp"

    cur_fp = _fingerprint(workflow)
    prev_fp = st.session_state.get(fp_key)
    changed = cur_fp != prev_fp

    if changed:
        # 从已有画布状态中保留位置
        pos_map: dict[str, tuple] = {}
        if state_key in st.session_state:
            for n in st.session_state[state_key].nodes:
                p = n.position
                pos_map[n.id] = (p["x"], p["y"]) if isinstance(p, dict) else p

        flow_nodes = []
        for node in workflow.nodes:
            pos = pos_map.get(node.id, node.position)
            flow_nodes.append(StreamlitFlowNode(
                id=node.id, pos=pos,
                data={"content": _node_content(node)},
                node_type="default",
                source_position="bottom", target_position="top",
                draggable=True, selectable=True,
                deletable=True, connectable=True,
                style=_node_style(node.agent_id, node.status),
            ))

        flow_edges = [
            StreamlitFlowEdge(
                id=e.id, source=e.source, target=e.target,
                edge_type="smoothstep", animated=True, deletable=True,
                marker_end={"type": "arrowclosed"},
                style={"stroke": "#90a4ae", "strokeWidth": "2"},
            )
            for e in workflow.edges
        ]

        st.session_state[state_key] = StreamlitFlowState(flow_nodes, flow_edges)
        st.session_state[fp_key] = cur_fp

    # 始终 ManualLayout — 不触发 ELK 重算
    updated = streamlit_flow(
        key=f"wf_canvas_{workflow.id}",
        state=st.session_state[state_key],
        height=420,
        fit_view=False,
        show_controls=True,
        show_minimap=False,
        allow_new_edges=True,
        animate_new_edges=True,
        layout=ManualLayout(),
        get_node_on_click=True,
        get_edge_on_click=True,
        pan_on_drag=True,
        allow_zoom=True,
        enable_node_menu=True,
        enable_edge_menu=True,
        hide_watermark=True,
        min_zoom=0.3,
    )

    if updated:
        st.session_state[state_key] = updated
        node_ids_after = {n.id for n in updated.nodes}

        umap = {n.id: n for n in updated.nodes}
        for node in workflow.nodes:
            if node.id in umap:
                p = umap[node.id].position
                node.position = (p["x"], p["y"]) if isinstance(p, dict) else p

        old_ids = {e.id for e in workflow.edges}
        synced = []
        for ue in updated.edges:
            if ue.id in old_ids:
                synced.append(next(e for e in workflow.edges if e.id == ue.id))
            else:
                synced.append(WorkflowEdge(id=ue.id, source=ue.source, target=ue.target))
        workflow.edges = synced
        workflow.nodes = [n for n in workflow.nodes if n.id in node_ids_after]

        if updated.selected_id:
            st.session_state["wf_selected_node"] = updated.selected_id

        st.session_state[fp_key] = _fingerprint(workflow)

    return workflow


# ══════════════════════════════════════
# 侧边栏 Agent 面板（点击 + 添加到画布）
# ══════════════════════════════════════

def render_sidebar_agent_palette(workflow: WorkflowDefinition) -> None:
    """侧边栏按类别展示所有 Agent，点击即添加到画布"""
    categories = settings.agent_registry.get("categories", {})
    for cat_key, cat_val in categories.items():
        cat_name = cat_val.get("name", cat_key)
        agents = cat_val.get("agents", [])

        with st.expander(f"{cat_key} {cat_name}", expanded=False):
            for a in agents:
                aid = a["id"]
                name = a["name"]
                on_canvas = any(n.agent_id == aid for n in workflow.nodes)
                label = f"{aid} {name}" + (" ●" if on_canvas else "")
                if st.button(
                    label, key=f"sb_node_{aid}",
                    use_container_width=True,
                    disabled=False,
                    help=a.get("description", ""),
                ):
                    pos = _calc_new_position(workflow)
                    node = WorkflowNode(
                        id=f"node_{short_id()}",
                        agent_id=aid,
                        label=get_agent_label(aid),
                        position=pos,
                        knowledge_ids=a.get("knowledge", []),
                    )
                    workflow.nodes.append(node)
                    st.session_state["wf_current"] = workflow
                    st.rerun()


# ══════════════════════════════════════
# 节点编辑面板
# ══════════════════════════════════════

def render_node_editor(workflow: WorkflowDefinition) -> None:
    sid = st.session_state.get("wf_selected_node")
    if not sid:
        return
    node = workflow.get_node(sid)
    if not node:
        return

    info = settings.get_agent_info(node.agent_id)
    name = info["name"] if info else node.agent_id
    desc = info.get("description", "") if info else ""
    cat = node.agent_id[0].upper()
    _, border = _CAT_COLORS.get(cat, ("#f5f5f5", "#bdbdbd"))

    hcol1, hcol2 = st.columns([6, 1])
    with hcol1:
        st.markdown(
            f'<span style="border-left:4px solid {border};padding-left:8px">'
            f'<b>{node.agent_id} {name}</b>'
            f'<span style="color:#888;margin-left:8px;font-size:0.85em">{desc}</span></span>',
            unsafe_allow_html=True,
        )
    with hcol2:
        if st.button("✕ 关闭", key="wf_close_ed", use_container_width=True):
            st.session_state.pop("wf_selected_node", None)
            st.rerun()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**📚 知识库**")
        kbs = list(settings.cloud_knowledge_config.get("mapping", {}).keys())
        if kbs:
            default = info.get("knowledge", []) if info else []
            cur = node.knowledge_ids if node.knowledge_ids else default
            node.knowledge_ids = st.multiselect(
                "知识库", kbs, default=[k for k in cur if k in kbs],
                key=f"ed_kb_{sid}", label_visibility="collapsed",
            )
        else:
            st.caption("暂无可用知识库")
    with c2:
        st.markdown("**🔗 参考 URL**")
        urls = st.text_area(
            "URL", value="\n".join(node.reference_urls), height=90,
            key=f"ed_url_{sid}", label_visibility="collapsed",
            placeholder="每行一个 URL",
        )
        node.reference_urls = [u.strip() for u in urls.strip().splitlines() if u.strip()]
    with c3:
        st.markdown("**⚙️ 参数**")
        txt = st.text_area(
            "参数", value="\n".join(f"{k}={v}" for k, v in node.custom_params.items()),
            height=90, key=f"ed_p_{sid}", label_visibility="collapsed",
            placeholder="key=value（每行一个）",
        )
        node.custom_params = {}
        for line in txt.strip().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                node.custom_params[k.strip()] = v.strip()


# ══════════════════════════════════════
# 执行结果
# ══════════════════════════════════════

def render_execution_results(
    workflow: WorkflowDefinition,
    results: dict[str, dict[str, Any]],
) -> None:
    if not results:
        return
    done = [n for n in workflow.nodes if n.id in results and n.status == NodeStatus.COMPLETED]
    fail = [n for n in workflow.nodes if n.id in results and n.status == NodeStatus.FAILED]
    if not done and not fail:
        return

    st.markdown("---")
    st.subheader("执行结果")
    labels = [n.agent_id for n in done] + [f"{n.agent_id}(失败)" for n in fail] + ["合并输出"]
    tabs = st.tabs(labels)

    for i, n in enumerate(done):
        with tabs[i]:
            st.markdown(results.get(n.id, {}).get("content", ""))
    for i, n in enumerate(fail):
        with tabs[len(done) + i]:
            st.error(results.get(n.id, {}).get("error", "未知错误"))
    with tabs[-1]:
        parts = []
        for n in done:
            c = results.get(n.id, {}).get("content", "")
            if c:
                parts.append(f"# {get_agent_label(n.agent_id)}\n\n{c}")
        if parts:
            merged = "\n\n---\n\n".join(parts)
            st.markdown(merged)
            st.download_button("下载合并 Markdown", merged,
                               file_name=f"workflow_{workflow.name}.md",
                               mime="text/markdown", key="wf_dl_merged")
        else:
            st.info("暂无已完成的输出")


# ══════════════════════════════════════
# 预设模板
# ══════════════════════════════════════

def build_preset_from_pipeline(start_id: str) -> WorkflowDefinition | None:
    chain: list[str] = []
    cur = start_id
    while cur:
        info = settings.get_agent_info(cur)
        if not info:
            break
        chain.append(cur)
        cur = info.get("pipeline_next")
        if cur in chain:
            break
    if not chain:
        return None

    nodes, edges = [], []
    for i, aid in enumerate(chain):
        info = settings.get_agent_info(aid)
        nodes.append(WorkflowNode(
            id=f"node_{short_id()}", agent_id=aid,
            label=get_agent_label(aid),
            position=(250, 50 + i * 100),
            knowledge_ids=info.get("knowledge", []) if info else [],
        ))
        if i > 0:
            edges.append(WorkflowEdge(
                id=f"edge_{short_id()}", source=nodes[i - 1].id, target=nodes[-1].id,
            ))

    cat_key = start_id[0]
    cat_name = settings.agent_registry.get("categories", {}).get(cat_key, {}).get("name", "管线")
    return WorkflowDefinition(
        id=f"preset_{short_id()}",
        name=f"{cat_name}管线 ({start_id}→{chain[-1]})",
        description=f"从 {start_id} 到 {chain[-1]} 的自动管线",
        nodes=nodes, edges=edges,
    )


def get_preset_pipelines() -> dict[str, str]:
    has_next, is_next = set(), set()
    for cat in settings.agent_registry.get("categories", {}).values():
        for a in cat.get("agents", []):
            if a.get("pipeline_next"):
                has_next.add(a["id"])
                is_next.add(a["pipeline_next"])
    presets = {}
    for sid in sorted(has_next - is_next):
        chain = [sid]
        cur = settings.get_agent_info(sid)
        while cur and cur.get("pipeline_next"):
            nxt = cur["pipeline_next"]
            if nxt in chain:
                break
            chain.append(nxt)
            cur = settings.get_agent_info(nxt)
        cat_name = settings.agent_registry.get("categories", {}).get(sid[0], {}).get("name", sid[0])
        presets[f"{cat_name}: {'→'.join(chain)}"] = sid
    return presets
