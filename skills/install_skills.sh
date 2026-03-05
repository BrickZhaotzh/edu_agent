#!/bin/bash
# 安装所有 Claude Code Skill 文件到 ~/.claude/skills/
# 使用方法: bash skills/install_skills.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_TARGET="$HOME/.claude/skills"

mkdir -p "$SKILLS_TARGET"

count=0
for skill_file in "$SCRIPT_DIR"/kc-*.md; do
    if [ -f "$skill_file" ]; then
        filename=$(basename "$skill_file")
        ln -sf "$skill_file" "$SKILLS_TARGET/$filename"
        echo "  已链接: $filename"
        count=$((count + 1))
    fi
done

echo ""
echo "完成！共安装 $count 个 Skill 文件到 $SKILLS_TARGET"
echo "使用方法: 在 Claude Code 中输入 /kc-<agent-id> 调用对应智能体"
