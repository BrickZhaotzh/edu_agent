"""对话式交互界面组件 — 支持流式输出 + 附件上传 + 多对话管理"""

import io
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st
from pydantic import BaseModel

# 确保项目根目录在 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.base_agent import BaseAgent
from src.core.chat_storage import ChatStorage
from src.core.config import settings

# 全局存储实例
_chat_storage = ChatStorage()


# ── 附件读取 ──

_TEXT_SUFFIXES = {".txt", ".md", ".csv", ".json", ".yaml", ".yml", ".xml", ".html", ".htm"}


def _read_uploaded_file(uploaded_file) -> str:
    """读取上传文件内容为文本"""
    suffix = Path(uploaded_file.name).suffix.lower()

    # 纯文本类
    if suffix in _TEXT_SUFFIXES:
        raw = uploaded_file.getvalue()
        for enc in ("utf-8", "gbk", "gb2312", "latin-1"):
            try:
                return raw.decode(enc)
            except (UnicodeDecodeError, LookupError):
                continue
        return raw.decode("utf-8", errors="replace")

    # DOCX
    if suffix in (".docx", ".doc"):
        try:
            from docx import Document
            doc = Document(io.BytesIO(uploaded_file.getvalue()))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except ImportError:
            return f"[无法解析 {uploaded_file.name}，缺少 python-docx]"

    # PDF
    if suffix == ".pdf":
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
            pages = [p.extract_text() or "" for p in reader.pages]
            return "\n\n".join(pages)
        except ImportError:
            return f"[无法解析 {uploaded_file.name}，缺少 PyPDF2]"

    # XLSX
    if suffix in (".xlsx", ".xls"):
        try:
            import pandas as pd
            df = pd.read_excel(io.BytesIO(uploaded_file.getvalue()))
            return df.to_markdown(index=False)
        except ImportError:
            return f"[无法解析 {uploaded_file.name}，缺少 pandas/openpyxl]"

    return f"[不支持的文件类型: {suffix}]"


def _render_field(field_name: str, config: dict, key: str) -> Any:
    """渲染单个输入字段并返回其值"""
    label = config.get("label", field_name)
    field_type = config.get("type", "text")
    default = config.get("default", "")
    help_text = config.get("help", "")

    if field_type == "text":
        return st.text_input(label, value=default, help=help_text, key=f"{key}_{field_name}")
    elif field_type == "textarea":
        return st.text_area(label, value=default, help=help_text, key=f"{key}_{field_name}")
    elif field_type == "select":
        options = config.get("options", [])
        return st.selectbox(label, options, help=help_text, key=f"{key}_{field_name}")
    elif field_type == "multiselect":
        options = config.get("options", [])
        return st.multiselect(label, options, default=default, help=help_text, key=f"{key}_{field_name}")
    elif field_type == "number":
        return st.number_input(label, value=default, help=help_text, key=f"{key}_{field_name}")
    elif field_type == "slider":
        min_val = config.get("min", 0)
        max_val = config.get("max", 100)
        return st.slider(label, min_val, max_val, default, help=help_text, key=f"{key}_{field_name}")
    return default


# ── Skill 查看 / 编辑 / 重置 ──

_SKILLS_DIR = project_root / "skills"
_CUSTOM_SKILLS_DIR = project_root / "data" / "custom_skills"


def _get_skill_paths(agent_id: str) -> tuple[Path | None, Path | None]:
    """根据 agent_id 查找默认和自定义 Skill 文件路径"""
    prefix = f"kc-{agent_id.lower()}-"
    default_path = None
    for f in _SKILLS_DIR.iterdir():
        if f.name.startswith(prefix) and f.suffix == ".md":
            default_path = f
            break
    if default_path is None:
        return None, None
    custom_path = _CUSTOM_SKILLS_DIR / default_path.name
    return default_path, custom_path


def _render_skill_editor(agent_id: str, key: str) -> None:
    """渲染 Skill 描述的查看/编辑/保存/重置 UI"""
    default_path, custom_path = _get_skill_paths(agent_id)
    if default_path is None:
        return

    is_custom = custom_path is not None and custom_path.exists()
    if is_custom:
        current_content = custom_path.read_text(encoding="utf-8")
    else:
        current_content = default_path.read_text(encoding="utf-8")

    editor_key = f"{key}_skill_editor"

    with st.expander("📝 Skill 描述", expanded=False):
        if is_custom:
            st.info("当前使用自定义 Skill（点击「重置为默认」可恢复）")

        edited = st.text_area(
            "Skill 内容",
            value=current_content,
            height=400,
            key=editor_key,
            label_visibility="collapsed",
        )

        col_save, col_reset, _ = st.columns([1, 1, 2])
        with col_save:
            if st.button("💾 保存", key=f"{key}_skill_save"):
                _CUSTOM_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
                custom_path.write_text(edited, encoding="utf-8")
                st.success("已保存")
                if editor_key in st.session_state:
                    del st.session_state[editor_key]
                st.rerun()
        with col_reset:
            if is_custom:
                if st.button("🔄 重置为默认", key=f"{key}_skill_reset"):
                    custom_path.unlink()
                    if editor_key in st.session_state:
                        del st.session_state[editor_key]
                    st.success("已重置")
                    st.rerun()


# ── 对话管理 ──


def _auto_save_current(key: str, agent_id: str) -> None:
    """将当前对话自动保存到磁盘"""
    messages = st.session_state.get(f"{key}_messages", [])
    if not messages:
        return

    conv_id = st.session_state.get(f"{key}_conv_id")
    if conv_id is None:
        conv_id = ChatStorage.generate_id()
        st.session_state[f"{key}_conv_id"] = conv_id
        st.session_state[f"{key}_conv_created"] = datetime.now().isoformat()

    first_user = next((m["content"] for m in messages if m["role"] == "user"), "")
    conversation = {
        "id": conv_id,
        "agent_id": agent_id,
        "title": ChatStorage.generate_title(first_user),
        "created_at": st.session_state.get(f"{key}_conv_created", datetime.now().isoformat()),
        "messages": messages,
    }
    _chat_storage.save(agent_id, conversation)


def _load_conversation(key: str, agent_id: str, conv_id: str) -> None:
    """从磁盘加载对话到 session state"""
    _auto_save_current(key, agent_id)

    data = _chat_storage.load(agent_id, conv_id)
    if data:
        st.session_state[f"{key}_messages"] = data.get("messages", [])
        st.session_state[f"{key}_conv_id"] = conv_id
        st.session_state[f"{key}_conv_created"] = data.get("created_at", "")
        assistant_msgs = [m for m in data.get("messages", []) if m["role"] == "assistant"]
        st.session_state[f"{key}_last_output"] = assistant_msgs[-1]["content"] if assistant_msgs else None
    else:
        st.session_state[f"{key}_messages"] = []
        st.session_state[f"{key}_conv_id"] = None
        st.session_state[f"{key}_last_output"] = None


def _render_conversation_sidebar(key: str, agent_id: str) -> None:
    """在侧边栏渲染当前 Agent 的对话历史管理面板"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("#### 💬 对话记录")

        if st.button("➕ 新建对话", key=f"{key}_new_conv", use_container_width=True):
            _auto_save_current(key, agent_id)
            st.session_state[f"{key}_messages"] = []
            st.session_state[f"{key}_last_output"] = None
            st.session_state[f"{key}_conv_id"] = None
            st.rerun()

        conversations = _chat_storage.list_conversations(agent_id)
        current_conv_id = st.session_state.get(f"{key}_conv_id")

        for conv in conversations:
            col_title, col_del = st.columns([5, 1])
            with col_title:
                label = conv["title"]
                if conv["id"] == current_conv_id:
                    label = f"▶ {label}"
                if st.button(label, key=f"{key}_load_{conv['id']}", use_container_width=True):
                    _load_conversation(key, agent_id, conv["id"])
                    st.rerun()
            with col_del:
                if st.button("🗑", key=f"{key}_del_{conv['id']}"):
                    _chat_storage.delete(agent_id, conv["id"])
                    if current_conv_id == conv["id"]:
                        st.session_state[f"{key}_messages"] = []
                        st.session_state[f"{key}_last_output"] = None
                        st.session_state[f"{key}_conv_id"] = None
                    st.rerun()

        if not conversations:
            st.caption("暂无历史对话")


def render_chat_interface(
    agent: BaseAgent,
    input_model: type[BaseModel],
    input_fields: dict[str, dict[str, Any]],
    session_key: str | None = None,
    show_export: bool = True,
):
    """渲染对话式交互界面

    Args:
        agent: Agent 实例
        input_model: 输入模型类
        input_fields: 输入字段配置 {field_name: {label, type, default, options, help}}
        session_key: session state 键前缀
        show_export: 是否显示导出按钮
    """
    key = session_key or agent.agent_id

    # 初始化 session state
    if f"{key}_messages" not in st.session_state:
        st.session_state[f"{key}_messages"] = []
    if f"{key}_last_output" not in st.session_state:
        st.session_state[f"{key}_last_output"] = None
    if f"{key}_conv_id" not in st.session_state:
        st.session_state[f"{key}_conv_id"] = None

    # 侧边栏对话管理面板
    _render_conversation_sidebar(key, agent.agent_id)

    # ── 设置面板（按钮切换显示/隐藏） ──
    field_values = {}
    persist_key = f"{key}_persisted_fields"
    if persist_key not in st.session_state:
        st.session_state[persist_key] = {}

    has_skill = _get_skill_paths(agent.agent_id)[0] is not None
    has_settings = bool(input_fields) or has_skill

    if has_settings:
        show_settings = st.toggle("⚙️ 设置", key=f"{key}_show_settings")
    else:
        show_settings = False

    if show_settings:
        with st.container(border=True):
            if input_fields:
                compact = [(n, c) for n, c in input_fields.items()
                           if c.get("type", "text") not in ("textarea", "multiselect")]
                wide = [(n, c) for n, c in input_fields.items()
                        if c.get("type", "text") in ("textarea", "multiselect")]

                for i in range(0, len(compact), 3):
                    batch = compact[i:i + 3]
                    cols = st.columns(len(batch))
                    for col, (name, cfg) in zip(cols, batch):
                        with col:
                            field_values[name] = _render_field(name, cfg, key)

                for name, cfg in wide:
                    field_values[name] = _render_field(name, cfg, key)

                # 持久化当前值，关闭面板后仍可用
                st.session_state[persist_key] = dict(field_values)

            if has_skill:
                _render_skill_editor(agent.agent_id, key)
    elif input_fields:
        # 面板关闭时从持久化中恢复参数值
        for name, cfg in input_fields.items():
            field_values[name] = st.session_state[persist_key].get(
                name, cfg.get("default", "")
            )

    # 显示历史消息
    for msg in st.session_state[f"{key}_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 知识库选择 + 附件上传
    kb_mapping = settings.cloud_knowledge_config.get("mapping", {})
    if kb_mapping:
        col_kb, col_file = st.columns(2)
        with col_kb:
            all_kbs = list(kb_mapping.keys())
            agent_info = settings.get_agent_info(agent.agent_id)
            agent_default = agent_info.get("knowledge", []) if agent_info else []
            valid_default = [k for k in agent_default if k in all_kbs]
            selected_kbs = st.multiselect(
                "📚 知识库", all_kbs, default=valid_default,
                key=f"{key}_knowledge_ids",
                help="选择知识库作为参考（可选）",
            )
            field_values["knowledge_ids"] = selected_kbs
        with col_file:
            uploaded = st.file_uploader(
                "上传参考资料",
                type=["txt", "md", "csv", "json", "pdf", "docx", "doc", "xlsx", "xls"],
                key=f"{key}_file_upload",
                label_visibility="collapsed",
                help="支持 txt/md/csv/json/pdf/docx/xlsx，作为参考资料随消息发送",
            )
    else:
        uploaded = st.file_uploader(
            "上传参考资料",
            type=["txt", "md", "csv", "json", "pdf", "docx", "doc", "xlsx", "xls"],
            key=f"{key}_file_upload",
            label_visibility="collapsed",
            help="支持 txt/md/csv/json/pdf/docx/xlsx，作为参考资料随消息发送",
        )

    user_input = st.chat_input(f"请输入您的需求（{agent.agent_name}）")

    if user_input:
        # 处理附件
        file_content = None
        file_name = None
        if uploaded:
            file_name = uploaded.name
            file_content = _read_uploaded_file(uploaded)

        # 显示用户消息
        display_msg = user_input
        if file_name:
            display_msg = f"📎 **{file_name}**\n\n{user_input}"
        st.session_state[f"{key}_messages"].append({"role": "user", "content": display_msg})
        with st.chat_message("user"):
            st.markdown(display_msg)

        # 构建输入
        field_values["query"] = user_input
        if file_content:
            field_values["file_content"] = file_content
            field_values["file_name"] = file_name
        try:
            input_data = input_model(**field_values)
        except Exception as e:
            st.error(f"输入参数错误: {e}")
            return

        # 流式输出
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            try:
                for chunk in agent.run_stream(input_data):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
                if not full_response:
                    full_response = "⚠️ 模型未返回内容，请稍后重试。"
                placeholder.markdown(full_response)
            except Exception as e:
                error_msg = f"⚠️ 调用失败: {e}"
                placeholder.markdown(error_msg)
                full_response = error_msg

        st.session_state[f"{key}_messages"].append({"role": "assistant", "content": full_response})
        st.session_state[f"{key}_last_output"] = full_response

        # 自动保存对话到磁盘
        _auto_save_current(key, agent.agent_id)

    # 导出按钮
    if show_export and st.session_state[f"{key}_last_output"]:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                "📄 下载 Markdown",
                st.session_state[f"{key}_last_output"],
                file_name=f"{agent.agent_id}_output.md",
                mime="text/markdown",
            )
        with col2:
            if st.button("📝 导出 Word", key=f"{key}_export_word"):
                from src.core.document_gen import DocumentGenerator
                doc = DocumentGenerator()
                output_model = agent.output_model(
                    agent_id=agent.agent_id,
                    agent_name=agent.agent_name,
                    content=st.session_state[f"{key}_last_output"],
                )
                path = agent.export_word(output_model)
                st.success(f"已导出: {path}")
