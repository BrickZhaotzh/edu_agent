"""E1.4 语音合成 — TTS脚本准备与语音合成配置"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class TTSGenAgent(BaseAgent):
    """语音合成智能体

    将教学逐字稿优化为TTS友好格式，生成语音合成脚本、
    标注停顿/语气/语速控制信息，并输出TTS配置参数。
    """

    agent_id = "E1.4"
    agent_name = "语音合成"
    system_prompt_template = "category_e/tts_gen_system.j2"
    user_prompt_template = "category_e/tts_gen_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context["input"]
        kb_text = ""
        if context.get("knowledge"):
            kb_text = "\n".join(
                f"### {k}\n{v}" for k, v in context["knowledge"].items()
            )

        upstream_text = ""
        if context.get("upstream"):
            upstream_text = f"\n## 上游输入\n{context['upstream']}"

        return f"""请根据以下内容，生成TTS语音合成脚本与配置。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请输出：
1. **TTS优化脚本**：将原始文本转换为TTS友好格式
   - 数字、缩写、专有名词的读音标注
   - 停顿标记（短停/长停/段落停顿）
   - 语气标注（平述/强调/疑问/感叹）
2. **分段脚本**：按教学环节拆分，每段标注预估时长
3. **TTS配置参数建议**：
   - 推荐音色（男声/女声/儿童声）
   - 语速设置（正常/慢速/分段变速）
   - 音量与音调参数
4. **SSML标记版本**：输出带SSML标签的脚本（兼容主流TTS引擎）
5. **质检要点**：需人工复核的发音、停顿、语气要点"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(TTSGenAgent, AgentInput)
