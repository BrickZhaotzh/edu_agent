"""首页仪表盘"""

import sys
from pathlib import Path

import streamlit as st

# 确保项目根目录在 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.config import settings

st.title("科创课程AI智能体平台")
st.markdown("---")

# 类别概览
categories = settings.agent_registry.get("categories", {})

cols = st.columns(3)
cat_icons = {"A": "📋", "B": "📐", "C": "🔬", "D": "🔧", "E": "🎬", "F": "📢"}

for i, (cat_key, cat_info) in enumerate(categories.items()):
    with cols[i % 3]:
        agents = cat_info.get("agents", [])
        p0_count = sum(1 for a in agents if a.get("priority") == "P0")
        st.metric(
            label=f"{cat_icons.get(cat_key, '📦')} {cat_key}类 · {cat_info['name']}",
            value=f"{len(agents)} 个智能体",
            delta=f"{p0_count} 个P0" if p0_count else None,
        )

st.markdown("---")

# 智能体清单表格
st.subheader("全部智能体一览")

all_agents = []
for cat_key, cat_info in categories.items():
    for agent in cat_info.get("agents", []):
        all_agents.append({
            "类别": f"{cat_key} · {cat_info['name']}",
            "ID": agent["id"],
            "名称": agent["name"],
            "优先级": agent["priority"],
            "描述": agent["description"],
        })

if all_agents:
    import pandas as pd
    df = pd.DataFrame(all_agents)

    # 优先级筛选
    priorities = st.multiselect("按优先级筛选", ["P0", "P1", "P2", "P3"], default=["P0", "P1"])
    if priorities:
        df = df[df["优先级"].isin(priorities)]

    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"共 {len(df)} 个智能体")
