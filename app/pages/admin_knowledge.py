"""云端知识库管理页面"""

import sys
from pathlib import Path

import streamlit as st

# 确保项目根目录在 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.cloud_knowledge import CloudKnowledgeManager
from src.core.config import settings

st.header("云端知识库管理")

if not settings.cloud_knowledge_enabled:
    st.warning(
        "云端知识库功能未启用。请在 `config/settings.yaml` 中设置 "
        "`cloud_knowledge.enabled: true` 后重启应用。"
    )
    st.stop()

# 初始化管理器（缓存到 session）
if "cloud_kb_mgr" not in st.session_state:
    st.session_state.cloud_kb_mgr = CloudKnowledgeManager()
mgr: CloudKnowledgeManager = st.session_state.cloud_kb_mgr

tab_list, tab_create, tab_upload, tab_mapping = st.tabs(
    ["知识库列表", "创建知识库", "上传文档", "映射配置"]
)

# ==================== Tab 1: 知识库列表 ====================
with tab_list:
    if st.button("刷新列表", key="refresh_kb"):
        st.session_state.pop("kb_list_cache", None)

    if "kb_list_cache" not in st.session_state:
        try:
            st.session_state.kb_list_cache = mgr.list_knowledge_bases()
        except Exception as e:
            st.error(f"获取知识库列表失败: {e}")
            st.session_state.kb_list_cache = []

    kb_list = st.session_state.kb_list_cache
    if not kb_list:
        st.info("暂无云端知识库，请先创建。")
    else:
        for kb in kb_list:
            with st.expander(f"{kb['name']}（ID: {kb['id']}）"):
                st.write(f"**描述**: {kb.get('description', '-')}")
                st.write(f"**Embedding ID**: {kb.get('embedding_id', '-')}")

                # 文档列表
                try:
                    docs = mgr.list_documents(kb["id"])
                    if docs:
                        st.markdown("**文档:**")
                        for doc in docs:
                            st.write(
                                f"  {doc['name']}  "
                                f"（{doc.get('word_num', 0)}字, "
                                f"向量化: {doc.get('embedding_stat', '')}）"
                            )
                except Exception as e:
                    st.warning(f"获取文档列表失败: {e}")

                if st.button(f"删除知识库", key=f"del_kb_{kb['id']}"):
                    if mgr.delete_knowledge_base(kb["id"]):
                        st.success("已删除")
                        st.session_state.pop("kb_list_cache", None)
                        st.rerun()
                    else:
                        st.error("删除失败")

# ==================== Tab 2: 创建知识库 ====================
with tab_create:
    with st.form("create_kb_form"):
        kb_name = st.text_input("知识库名称", placeholder="如：K12政策文件库")
        kb_desc = st.text_area("描述（可选）", placeholder="存放教育政策相关文档")
        submitted = st.form_submit_button("创建")

    if submitted and kb_name:
        try:
            result = mgr.create_knowledge_base(kb_name, kb_desc)
            st.success(f"创建成功！知识库 ID: `{result['id']}`")
            st.info("请将此 ID 填入 `config/settings.yaml` 的 `cloud_knowledge.mapping` 中。")
            st.session_state.pop("kb_list_cache", None)
        except Exception as e:
            st.error(f"创建失败: {e}")

# ==================== Tab 3: 上传文档 ====================
with tab_upload:
    # 选择目标知识库
    if not kb_list:
        st.info("请先创建知识库。")
    else:
        kb_options = {f"{kb['name']}（{kb['id']}）": kb["id"] for kb in kb_list}
        selected_kb_label = st.selectbox("选择目标知识库", list(kb_options.keys()))
        selected_kb_id = kb_options[selected_kb_label]

        uploaded_file = st.file_uploader(
            "上传文档",
            type=["doc", "docx", "pdf", "xlsx", "txt", "md"],
            help="支持 doc/docx/pdf/xlsx/txt/md，单文件 ≤ 50MB",
        )

        if uploaded_file and st.button("确认上传"):
            # 保存临时文件
            import tempfile
            from pathlib import Path

            with tempfile.NamedTemporaryFile(
                delete=False, suffix=Path(uploaded_file.name).suffix
            ) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            try:
                with st.spinner("正在上传并处理..."):
                    result = mgr.upload_document(selected_kb_id, tmp_path)
                st.success(f"上传成功！文档 ID: `{result['document_id']}`")
                st.session_state.pop("kb_list_cache", None)
            except Exception as e:
                st.error(f"上传失败: {e}")
            finally:
                Path(tmp_path).unlink(missing_ok=True)

# ==================== Tab 4: 映射配置 ====================
with tab_mapping:
    st.subheader("当前映射关系")
    st.caption("编辑 `config/settings.yaml` → `cloud_knowledge.mapping` 修改映射。")

    mapping = settings.cloud_knowledge_config.get("mapping", {})
    if not mapping:
        st.info("尚未配置任何映射。")
    else:
        for local_id, cloud_id in mapping.items():
            st.write(f"- **{local_id}** → `{cloud_id}`")

    st.divider()
    st.markdown(
        "**配置示例**（写入 `config/settings.yaml`）:\n"
        "```yaml\n"
        "cloud_knowledge:\n"
        "  enabled: true\n"
        "  mapping:\n"
        "    policies: \"your_cloud_kb_id_here\"\n"
        "    competitor_reports: \"your_cloud_kb_id_here\"\n"
        "```"
    )
