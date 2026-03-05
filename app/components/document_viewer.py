"""文档预览组件"""

import streamlit as st


def render_document_viewer(content: str, title: str = "文档预览"):
    """渲染 Markdown 文档预览

    Args:
        content: Markdown 格式的文档内容
        title: 预览区域标题
    """
    if not content:
        st.info("暂无内容可预览")
        return

    st.subheader(title)

    # 选项卡切换：渲染视图 / 源码视图
    tab1, tab2 = st.tabs(["渲染视图", "Markdown 源码"])

    with tab1:
        st.markdown(content)

    with tab2:
        st.code(content, language="markdown")


def render_structured_data(data: dict, title: str = "结构化数据"):
    """渲染结构化数据（表格/JSON）"""
    if not data:
        return

    st.subheader(title)

    import pandas as pd

    if isinstance(data, list) and data and isinstance(data[0], dict):
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    elif isinstance(data, dict):
        # 嵌套 dict 显示为 JSON
        flat_items = {}
        for k, v in data.items():
            if isinstance(v, (list, dict)):
                flat_items[k] = str(v)
            else:
                flat_items[k] = v

        if all(not isinstance(v, (list, dict)) for v in data.values()):
            df = pd.DataFrame([data])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.json(data)
