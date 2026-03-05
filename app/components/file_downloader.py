"""文件下载组件"""

from pathlib import Path

import streamlit as st


def render_file_downloader(file_path: str | Path, label: str = "下载文件"):
    """渲染文件下载按钮

    Args:
        file_path: 文件路径
        label: 按钮文字
    """
    path = Path(file_path)
    if not path.exists():
        st.warning(f"文件不存在: {path}")
        return

    with open(path, "rb") as f:
        data = f.read()

    # 根据扩展名推断 MIME
    mime_map = {
        ".md": "text/markdown",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".pdf": "application/pdf",
        ".json": "application/json",
        ".txt": "text/plain",
    }
    mime = mime_map.get(path.suffix.lower(), "application/octet-stream")

    st.download_button(
        label=label,
        data=data,
        file_name=path.name,
        mime=mime,
    )


def render_multi_download(files: list[dict], title: str = "文件下载"):
    """渲染多文件下载区域

    Args:
        files: [{"path": "...", "label": "..."}]
        title: 标题
    """
    if not files:
        return

    st.subheader(title)
    cols = st.columns(min(len(files), 4))
    for i, file_info in enumerate(files):
        with cols[i % 4]:
            render_file_downloader(file_info["path"], file_info.get("label", "下载"))
