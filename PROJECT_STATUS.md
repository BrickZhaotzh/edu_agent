# 科创课程AI智能体平台 — 项目进度总结

> **作者**：BrickZhao (tzzhao3@iflytek.com)
> **更新时间**：2026-03-05（第二次更新）

---

## 一、项目概述

基于 GLM-4.7 大模型，构建覆盖科创课程开发全生命周期的 **6大类（A-F）、47个智能体** 系统。每个智能体同时提供 **Streamlit Web 界面** 和 **Claude Code Skill**（CLI）。

---

## 二、整体完成度

| 模块 | 状态 | 数量 |
|------|------|------|
| 核心基础设施 (src/core/) | ✅ 已完成 | 9个模块 |
| Agent 基类 | ✅ 已完成 | 1个 |
| A类 智能体 | ✅ 已完成 | 7个 |
| B类 智能体 | ✅ 已完成 | 7个 |
| C类 智能体 | ✅ 已完成 | 19个 |
| D类 智能体 | ✅ 已完成 | 4个 |
| E类 智能体 | ✅ 已完成 | 4个 |
| F类 智能体 | ✅ 已完成 | 6个 |
| Jinja2 提示词模板 | ✅ 已完成 | 94个（每个Agent 2个） |
| Streamlit 页面 | ✅ 已完成 | 47+3（首页+工作流+知识库管理） |
| Claude Code Skills | ✅ 已完成 | 47个 .md 文件 |
| 知识库链接 | ✅ 已完成 | 2个本地 + 云端知识库管理 |
| 对话持久化 | ✅ 已完成 | JSON 多对话存储 + 侧边栏管理 |
| 工作流编排引擎 | ✅ 已完成 | DAG 拓扑排序 + 流式执行 |
| 云端知识库管理 | ✅ 已完成 | 智谱 AI 知识库 CRUD + RAG 检索 |
| 参数设置面板 | ✅ 已完成 | 可折叠配置面板 + Skill 编辑器 |
| 文档导出组件 | ✅ 已完成 | Markdown/Word 导出 + 多文件下载 |
| 端到端 API 验证 | ✅ 已通过 | A1.1 同步 + A2.1 流式 |

**文件统计**：94 模板 + 47 Agent + 50 页面 + 47 Skill + 9 Core = **247 个核心文件**

---

## 三、项目结构

```
kechuang-ai-agents/
├── .env                          # API Key 及模型配置
├── config/
│   ├── settings.yaml             # 全局配置（模型/知识库/导出/UI）
│   └── agent_registry.yaml       # 47个智能体注册表（ID/名称/优先级/模块/管线依赖）
├── src/
│   ├── core/                     # 共享基础设施（9个模块）
│   │   ├── config.py             # YAML + .env 配置加载（Settings 单例）
│   │   ├── models.py             # 所有 Agent 的 Pydantic 输入/输出模型
│   │   ├── llm_client.py         # GLM-4.7 客户端（同步/流式/工具调用）
│   │   ├── prompt_engine.py      # Jinja2 模板渲染引擎
│   │   ├── knowledge_base.py     # 本地知识库加载与关键词检索
│   │   ├── cloud_knowledge.py    # 云端知识库管理（智谱AI RAG）
│   │   ├── chat_storage.py       # 对话持久化（JSON文件存储）
│   │   ├── workflow_engine.py    # 工作流 DAG 执行引擎
│   │   ├── workflow_models.py    # 工作流数据模型
│   │   ├── workflow_storage.py   # 工作流持久化
│   │   └── document_gen.py       # 文档导出（MD/DOCX/XLSX）
│   ├── agents/
│   │   ├── base_agent.py         # 抽象基类（run/run_stream/export）
│   │   ├── category_a/           # 7个 Agent（政策/竞品/痛点/立项/Demo/评分/资源）
│   │   ├── category_b/           # 7个 Agent（规划/课标/单元主题/细化/大纲/课时/交付）
│   │   ├── category_c/           # 19个 Agent（问题链/方案稿/逐字稿/分镜/课件/…）
│   │   ├── category_d/           # 4个 Agent（需求清单/示意图/规格书/寻源）
│   │   ├── category_e/           # 4个 Agent（说课视频/外包视频/搭建视频/语音合成）
│   │   └── category_f/           # 6个 Agent（海报/介绍/培训/运营/调研/FAQ）
│   ├── prompts/                  # Jinja2 提示词模板（94个，按类别分目录）
│   │   ├── category_a/           # 14个（每Agent 1 system + 1 user）
│   │   ├── category_b/           # 14个
│   │   ├── category_c/           # 38个
│   │   ├── category_d/           # 8个
│   │   ├── category_e/           # 8个
│   │   └── category_f/           # 12个
│   └── knowledge/                # 知识库（符号链接）
│       ├── policies -> ~/Documents/各省AI通识课指南/
│       └── competitor_reports -> ~/Documents/竞品调研报告/
├── app/                          # Streamlit 多页面应用
│   ├── app.py                    # 主入口（st.navigation 六大类导航）
│   ├── components/
│   │   ├── chat_interface.py     # 对话式交互界面（流式+持久化+设置面板+Skill编辑）
│   │   ├── workflow_canvas.py    # 工作流可视化画布
│   │   ├── document_viewer.py    # 文档双模式预览（渲染+源码）
│   │   └── file_downloader.py    # 多文件下载（自动MIME检测）
│   └── pages/                    # 50个页面
│       ├── home.py               # 首页仪表盘
│       ├── workflow_builder.py   # 工作流编排器（DAG可视化+执行）
│       ├── admin_knowledge.py    # 云端知识库管理后台
│       ├── category_a/           # 7个页面
│       ├── category_b/           # 7个页面
│       ├── category_c/           # 19个页面
│       ├── category_d/           # 4个页面
│       ├── category_e/           # 4个页面
│       └── category_f/           # 6个页面
├── skills/                       # Claude Code Skill 文件（47个 .md）
│   ├── install_skills.sh         # 安装脚本
│   └── kc-*.md                   # 每个Agent一个Skill
├── output/                       # 文档导出目录
├── requirements.txt
└── .gitignore
```

---

## 四、47个智能体清单

### A类 — 课程产品方案（7个）

| ID | 名称 | 优先级 | Agent 类 | 功能 |
|----|------|--------|----------|------|
| A1.1 | 政策洞察分析 | P0 | PolicyInsightAgent | 多渠道政策检索+课标映射+课程适配建议 |
| A2.1 | 行业竞品调研 | P0 | CompetitorResearchAgent | 竞品信息抓取+结构化对比+差异点提炼 |
| A2.2 | 用户痛点分析 | P1 | UserPainPointAgent | 调研问卷生成+数据分析+用户画像建模 |
| A3.1 | 课程立项书 | P1 | CourseProposalAgent | 商业模式框架+多方案推演+可行性分析 |
| A4.1 | Demo课设计 | P1 | DemoDesignAgent | 基于优秀课例知识库的课程设计 |
| A5.1 | Demo评分模型 | P2 | DemoScoringAgent | 多维度评分标准+自动评审 |
| A6.1 | 生态资源评估 | P2 | ResourceAssessmentAgent | 资源录入+分类标签+复用性评估 |

### B类 — 课程方案（7个，含管线 B1.2→B1.3→B1.4→B1.5→B2.1）

| ID | 名称 | 优先级 | Agent 类 | 功能 |
|----|------|--------|----------|------|
| B1.1 | 课程整体规划 | P1 | CoursePlanningAgent | 课程整体规划与设计 |
| B1.2 | 课标教材匹配 | P0 | StandardMatchingAgent | 课程标准与教材匹配分析 |
| B1.3 | 单元主题架构 | P0 | UnitThemeAgent | 单元主题架构设计 |
| B1.4 | 单元细化主题 | P0 | UnitDetailAgent | 单元主题细化与展开 |
| B1.5 | 大纲整合输出 | P0 | OutlineIntegrationAgent | 课程大纲整合与输出 |
| B2.1 | 单节课时设计 | P0 | LessonDesignAgent | 单节课时详细设计 |
| B2.2 | Demo课交付 | P3 | DemoDeliveryAgent | Demo课程交付与包装 |

### C类 — 教研量产（19个，含管线 C1.1→C1.3→C1.4）

| ID | 名称 | 优先级 | Agent 类 |
|----|------|--------|----------|
| C1.1 | 问题链设计 | P0 | QuestionChainAgent |
| C1.2 | 方案稿撰写 | P1 | ProposalDraftAgent |
| C1.3 | 逐字稿生成 | P0 | ScriptGenAgent |
| C1.4 | 分镜脚本 | P0 | StoryboardAgent |
| C1.5 | 课件生成 | P1 | SlideshowAgent |
| C1.6 | 教学设计 | P1 | TeachingDesignAgent |
| C1.7 | 学生手册 | P1 | StudentManualAgent |
| C1.8 | 教师手册 | P1 | TeacherManualAgent |
| C1.9 | 课后作业 | P1 | HomeworkAgent |
| C1.10 | 评价量规 | P1 | RubricAgent |
| C2.1 | 实验PRD | P1 | ExperimentPRDAgent |
| C2.2 | 编程样例 | P1 | CodeExampleAgent |
| C3.1 | 拼音标注 | P1 | PinyinAnnotatorAgent |
| C3.2 | 教学审核 | P1 | TeachingReviewAgent |
| C3.3 | 随堂练习 | P1 | ClassExerciseAgent |
| C3.4 | 微课评审 | P2 | MicroLessonReviewAgent |
| C4.1 | 资源上传 | P3 | ResourceUploadAgent |
| C5.1 | 知识图谱 | P2 | KnowledgeGraphAgent |
| C5.2 | 课标分析 | P1 | StandardAnalysisAgent |

### D类 — 学具制作（4个，管线 D1.1→D1.5）

| ID | 名称 | 优先级 | Agent 类 |
|----|------|--------|----------|
| D1.1 | 教具需求清单 | P1 | SupplyListAgent |
| D1.2 | 教具示意图 | P2 | SupplyDiagramAgent |
| D1.5 | 需求规格说明书 | P1 | RequirementSpecAgent |
| D2.1 | 学具寻源 | P2 | SupplySourcingAgent |

### E类 — 视频制作（4个）

| ID | 名称 | 优先级 | Agent 类 |
|----|------|--------|----------|
| E1.1 | 说课视频 | P2 | LectureVideoAgent |
| E1.2 | 外包视频制作 | P1 | OutsourceVideoAgent |
| E1.3 | 学具搭建视频 | P2 | AssemblyVideoAgent |
| E1.4 | 语音合成 | P1 | TTSGenAgent |

### F类 — 课程运营（6个）

| ID | 名称 | 优先级 | Agent 类 |
|----|------|--------|----------|
| F1.1 | 宣传海报文案 | P2 | PosterCopyAgent |
| F1.2 | 课程介绍页 | P2 | CourseIntroAgent |
| F1.3 | 培训材料 | P2 | TrainingMaterialAgent |
| F1.4 | 运营文案 | P1 | OperationCopyAgent |
| F2.1 | 满意度调研 | P1 | SatisfactionSurveyAgent |
| F3.1 | FAQ智能答疑 | P0 | FAQBotAgent |

---

## 五、技术要点

### GLM-4.7 推理模型适配

GLM-4.7 是推理模型，输出分为 `reasoning_content`（思考过程）和 `content`（最终回答）：

- `llm_client.py` 已做双路径处理：优先返回 `content`，若为空则回退到 `reasoning_content`
- `max_tokens` 需设为 **8192**（推理过程消耗大量 token，4096 会导致 content 为空）
- 流式模式仅返回 `content` 部分，全程无 content 时回退返回 reasoning

### 代理（Proxy）问题

- 机器有系统代理 `http_proxy=http://127.0.0.1:7897`
- **启动 Streamlit 时必须移除代理**，否则 ZhipuAI API 调用会失败
- 启动命令：

```bash
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
  streamlit run app/app.py --server.port 8501 --server.headless true
```

### 知识库

- `src/knowledge/policies` → `~/Documents/各省AI通识课指南/`（34省政策文件，约235个文本块）
- `src/knowledge/competitor_reports` → `~/Documents/竞品调研报告/`（约20个文本块）
- A1.1（政策洞察）和 A2.1（竞品调研）会自动加载对应知识库

### 管线（Pipeline）依赖

通过 `upstream_output` 字段实现前后级数据传递：

- **B类管线**：B1.2 → B1.3 → B1.4 → B1.5 → B2.1（课标→单元→细化→大纲→课时）
- **C类管线**：C1.1 → C1.3 → C1.4（问题链→逐字稿→分镜脚本）
- **D类管线**：D1.1 → D1.5（需求清单→规格说明书）

---

## 六、已验证的功能

| 测试项 | 结果 |
|--------|------|
| A1.1 政策洞察（同步调用） | ✅ 3063字完整报告 |
| A2.1 竞品调研（流式调用） | ✅ 4215字流式输出 |
| A1.1 政策洞察（流式，无代理） | ✅ 2530字流式输出 |
| 知识库加载（policies） | ✅ 235个文本块 |
| 知识库加载（competitor_reports） | ✅ 20个文本块 |
| Streamlit 启动 | ✅ localhost:8501 |
| 47个 Agent 模块 import | ✅ 全部通过 |
| 94个 Jinja2 模板渲染 | ✅ 全部通过 |

---

## 七、已修复问题

| 日期 | 问题 | 修复 |
|------|------|------|
| 03-04 | GLM-4.7 推理模型 content 为空 | llm_client.py 增加 reasoning_content 回退，max_tokens 提升至 8192 |
| 03-04 | Streamlit 中模型不回复 | 启动时移除 http_proxy 代理环境变量 |
| 03-04 | chat_interface 错误无提示 | 增加 try/except 错误显示和空回复提示 |
| 03-05 | 学段选项过于细分 | 统一为「全部/小学/初中/高中」四项（涉及 4 个页面） |

---

## 八、近期新增功能（03-05）

### 8.1 对话持久化 & 多对话管理

- **chat_storage.py**: JSON 文件存储，路径 `data/conversations/{agent_id}/conv_YYYYMMDD_HHmmss.json`
- **侧边栏对话面板**: 每个 Agent 页面底部显示「➕ 新建对话」+ 历史对话列表 + 🗑 删除
- 自动保存：助手回复后立即持久化；切换对话时自动保存当前对话
- 自动标题：从用户首条消息截取前 20 字作为对话标题
- 导航标题气泡：侧边栏 Agent 名称后显示对话计数 `(3)`

### 8.2 工作流编排引擎

- **workflow_models.py**: WorkflowNode / WorkflowEdge / WorkflowDefinition 数据模型
- **workflow_engine.py**: DAG 执行引擎 — Kahn 拓扑排序、环检测、流式执行、上游数据自动合并、错误隔离（上游失败→下游跳过）
- **workflow_storage.py**: 工作流 JSON 持久化
- **workflow_builder.py 页面**: 可视化编排 UI — Agent 选择面板、预设管线、节点编辑器、全局 Query 输入、逐节点流式执行进度

### 8.3 云端知识库管理

- **cloud_knowledge.py**: 对接智谱 AI 知识库 API — KB CRUD、文档上传（doc/pdf/xlsx/txt/md, ≤50MB）、RAG retrieval tool 构建
- **admin_knowledge.py 页面**: 管理后台 — 知识库列表/创建/文档上传/映射配置
- **Agent 集成**: base_agent.py 自动从 agent_registry + 用户输入获取 knowledge_ids，构建 retrieval tools

### 8.4 参数设置面板 & Skill 编辑器

- **可折叠设置面板**: ⚙️ 按钮切换显示/隐藏，支持 text/textarea/select/multiselect/number/slider 字段类型
- **Skill 查看/编辑**: 读取 `/skills/kc-{id}-.md` 默认 Skill，支持自定义编辑并保存到 `/data/custom_skills/`，可一键重置
- **知识库选择器**: 设置面板内选择云端知识库（从配置自动填充）

### 8.5 文档预览与导出

- **document_viewer.py**: 双模式预览（渲染视图 + Markdown 源码），结构化数据表格显示
- **file_downloader.py**: 单文件/多文件下载按钮，自动 MIME 类型检测

### 8.6 GitHub 仓库

- **地址**: https://github.com/BrickZhaotzh/edu_agent
- **首次提交**: 281 文件，19034 行代码

---

## 十、后续待办

### 优先级 P0（建议优先处理）

1. **逐个页面功能测试** — 在 Streamlit 中挨个打开 47 个页面，验证输入→调用→输出完整流程
2. **提示词质量优化** — 当前模板为初版，需根据实际输出质量逐个调优 Jinja2 模板
3. **管线页面联动** — B类和C类管线目前需手动复制上游输出，可考虑增加自动传递 UI

### 优先级 P1

4. **Claude Code Skill 安装与测试** — 运行 `skills/install_skills.sh` 将 Skill 链接到 `~/.claude/skills/`，在 CLI 中逐个验证
5. **Word/Excel 导出测试** — 验证 `document_gen.py` 的 DOCX/XLSX 导出功能
6. **错误处理增强** — 当前 chat_interface 已有基础错误显示，可进一步增加重试、超时提示
7. **模型参数页面调优** — 部分 Agent 可能需要不同的 temperature/max_tokens

### 优先级 P2

8. **知识库扩充** — 补充更多知识库来源（教材库、优秀课例库等）
9. **用户认证** — 为 Streamlit 添加登录功能
10. **部署方案** — 考虑 Docker 化或云部署

---

## 十一、快速启动

```bash
# 1. 安装依赖
cd ~/Documents/kechuang-ai-agents
pip install -r requirements.txt

# 2. 配置 API Key（已配置）
# .env 文件已包含 ZHIPUAI_API_KEY

# 3. 启动 Streamlit（必须移除代理）
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
  streamlit run app/app.py --server.port 8501 --server.headless true

# 4. 浏览器打开
open http://localhost:8501
```

---

## 十二、依赖版本

```
zhipuai>=2.1.0        # GLM-4.7 SDK
streamlit>=1.51.0     # Web UI
pydantic>=2.0.0       # 数据校验
jinja2>=3.1.0         # 模板引擎
pyyaml>=6.0           # YAML 配置
pandas>=2.0.0         # 数据处理
openpyxl>=3.1.0       # Excel 导出
python-docx>=1.0.0    # Word 导出
```
