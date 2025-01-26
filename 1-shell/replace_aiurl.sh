#!/bin/bash

replace_aiurl() {
  # 检查是否安装了gum
  if ! command -v gum &> /dev/null; then
    echo "错误：请先安装gum工具"
    echo "安装命令：brew install gum"
    return 1
  fi

  # 目标文件路径
  local TARGET_FILE="/home/song/.config/ml4w/settings/ai.sh"

  while true; do
    # 使用gum选择操作
    local ACTION=$(gum choose "替换URL" "查看当前URL" "退出")

    case $ACTION in
      "替换URL")
        # 获取当前URL
        local CURRENT_URL=$(grep -oE 'https?://[^[:space:]]+' "$TARGET_FILE" | head -n 1)
        
        # 如果没有找到URL，则查找--new-window
        if [[ -z "$CURRENT_URL" ]]; then
          gum style --foreground 214 "未找到URL，尝试查找--new-window"
          local WINDOW_LINE=$(grep -n -- '--new-window' "$TARGET_FILE" | head -n 1)
          
          if [[ -z "$WINDOW_LINE" ]]; then
            gum style --foreground 9 "未找到--new-window"
            continue
          fi
        fi

        # 显示当前URL并获取新URL
        gum style --foreground 212 "当前URL: ${CURRENT_URL:-未找到}"
        local NEW_URL=$(gum input --placeholder "请输入新的URL（留空则不修改）" --prompt "> " --value "$CURRENT_URL")

        # 如果输入为空，则保持原状
        if [[ -z "$NEW_URL" ]]; then
          gum style --foreground 214 "未修改URL，保持原状"
          continue
        fi

        # 执行替换或添加
        if [[ -n "$CURRENT_URL" ]]; then
          # 替换现有URL
          sed -i -E "s|${CURRENT_URL}|${NEW_URL}|g" "${TARGET_FILE}"
        else
          # 在--new-window后添加新URL
          sed -i "${WINDOW_LINE%%:*}"'s|\(--new-window\)|\1 '"${NEW_URL}"'|' "${TARGET_FILE}"
        fi

        # 检查是否成功
        if [ $? -eq 0 ]; then
          gum style --foreground 10 "URL替换/添加成功！"
          gum style "新URL: $NEW_URL"
        else
          gum style --foreground 9 "URL替换/添加失败"
        fi
        ;;

      "查看当前URL")
        local CURRENT_URL=$(grep -oE 'https?://[^[:space:]]+' "$TARGET_FILE" | head -n 1)
        if [[ -z "$CURRENT_URL" ]]; then
          gum style --foreground 214 "未找到URL"
        else
          gum style --foreground 212 "当前URL: $CURRENT_URL"
        fi
        ;;

      "退出")
        return 0
        ;;
    esac
  done
}

# 如果直接执行脚本，则调用函数
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  replace_aiurl
fi
