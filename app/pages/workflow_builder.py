"""工作流编排器 — 可视化拖拽 + 多 Agent 协同执行"""

import sys
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.workflow_engine import WorkflowEngine
from src.core.workflow_models import NodeStatus, WorkflowDefinition
from src.core.workflow_storage import WorkflowStorage

from app.components.workflow_canvas import (
    get_agent_label,
    build_preset_from_pipeline,
    get_preset_pipelines,
    render_execution_results,
    render_node_editor,
    render_sidebar_agent_palette,
    render_workflow_canvas,
)

# ── 初始化 ──

engine = WorkflowEngine()
storage = WorkflowStorage()

if "wf_current" not in st.session_state:
    st.session_state["wf_current"] = WorkflowDefinition(
        id=uuid.uuid4().hex[:12], name="新工作流",
    )
if "wf_results" not in st.session_state:
    st.session_state["wf_results"] = {}

workflow: WorkflowDefinition = st.session_state["wf_current"]

# ══════════════════════════════════════
# 侧边栏：Agent 面板 + 预设 + 管理
# ══════════════════════════════════════

with st.sidebar:
    render_sidebar_agent_palette(workflow)

    st.markdown("---")

    # 预设管线
    with st.expander("🚀 预设管线"):
        presets = get_preset_pipelines()
        for label, sid in presets.items():
            if st.button(label, key=f"wf_ps_{sid}", use_container_width=True):
                wf = build_preset_from_pipeline(sid)
                if wf:
                    st.session_state["wf_current"] = wf
                    st.session_state["wf_results"] = {}
                    st.session_state.pop("wf_selected_node", None)
                    st.rerun()

    # 工作流管理
    with st.expander("💾 保存 / 加载"):
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("保存", key="wf_save", use_container_width=True):
                workflow.updated_at = datetime.now()
                storage.save(workflow)
                st.toast("已保存")
        with sc2:
            if st.button("新建", key="wf_new", use_container_width=True):
                st.session_state["wf_current"] = WorkflowDefinition(
                    id=uuid.uuid4().hex[:12], name="新工作流",
                )
                st.session_state["wf_results"] = {}
                st.session_state.pop("wf_selected_node", None)
                st.rerun()

        saved = storage.list_all()
        if saved:
            opts = {f"{w['name']} ({w['node_count']}节点)": w["id"] for w in saved}
            sel = st.selectbox("已保存", list(opts.keys()), key="wf_load_sel", label_visibility="collapsed")
            lc1, lc2 = st.columns(2)
            with lc1:
                if st.button("加载", key="wf_load_go", use_container_width=True):
                    loaded = storage.load(opts[sel])
                    if loaded:
                        st.session_state["wf_current"] = loaded
                        st.session_state["wf_results"] = {}
                        st.session_state.pop("wf_selected_node", None)
                        st.rerun()
            with lc2:
                if st.button("删除", key="wf_del", use_container_width=True):
                    storage.delete(opts[sel])
                    st.rerun()

# ══════════════════════════════════════
# 主区域
# ══════════════════════════════════════

# 标题 + 工作流名称
tc1, tc2 = st.columns([1, 2])
with tc1:
    st.markdown('<h2 style="margin:0">工作流编排器</h2>', unsafe_allow_html=True)
with tc2:
    new_name = st.text_input(
        "名称", value=workflow.name, key="wf_name",
        label_visibility="collapsed", placeholder="工作流名称",
    )
    if new_name != workflow.name:
        workflow.name = new_name

# 画布
if workflow.nodes:
    workflow = render_workflow_canvas(workflow)
    st.session_state["wf_current"] = workflow
else:
    st.info("从左侧面板点击 ＋ 添加 Agent 节点，或加载预设管线。")

# 节点编辑面板
if st.session_state.get("wf_selected_node") and workflow.get_node(st.session_state["wf_selected_node"]):
    st.markdown("---")
    render_node_editor(workflow)
    st.session_state["wf_current"] = workflow

# ── 执行区 ──

st.markdown("---")
eq, er, eres = st.columns([4, 1, 1])

with eq:
    q = st.text_input(
        "Query", value=workflow.global_query, key="wf_q",
        label_visibility="collapsed", placeholder="输入 Query 驱动所有节点...",
    )
    workflow.global_query = q

with er:
    run = st.button("▶ 执行", disabled=not workflow.nodes or not q,
                     type="primary", key="wf_run", use_container_width=True)

with eres:
    if st.button("↺ 重置", key="wf_reset", use_container_width=True):
        for n in workflow.nodes:
            n.status = NodeStatus.PENDING
            n.output = None
        st.session_state["wf_results"] = {}
        st.rerun()

if run and workflow.nodes and q:
    errors = engine.validate(workflow)
    if errors:
        for e in errors:
            st.error(e)
    else:
        for n in workflow.nodes:
            n.status = NodeStatus.PENDING
            n.output = None

        order = engine.topological_sort(workflow)
        results: dict = {}
        st.session_state["wf_results"] = results
        bar = st.progress(0, text="准备执行...")

        for idx, nid in enumerate(order):
            node = workflow.get_node(nid)
            if not node:
                continue
            label = node.label or get_agent_label(node.agent_id)
            bar.progress(idx / len(order), text=f"{label} ({idx+1}/{len(order)})")

            ups = workflow.get_upstream_nodes(nid)
            if any(u.status in (NodeStatus.FAILED, NodeStatus.SKIPPED) for u in ups):
                node.status = NodeStatus.SKIPPED
                results[nid] = {"skipped": True}
                continue

            node.status = NodeStatus.RUNNING
            with st.expander(f"⏳ {label}", expanded=True):
                ph = st.empty()
                txt = ""
                try:
                    for chunk in engine.execute_node_stream(workflow, nid, q, results):
                        txt += chunk
                        ph.markdown(txt + "▌")
                    ph.markdown(txt)
                except Exception as exc:
                    node.status = NodeStatus.FAILED
                    node.output = {"error": str(exc)}
                    results[nid] = {"error": str(exc)}
                    st.error(f"{label} 失败: {exc}")

        bar.progress(1.0, text="执行完成!")
        st.session_state["wf_results"] = results
        st.session_state["wf_current"] = workflow

render_execution_results(workflow, st.session_state.get("wf_results", {}))
