#!/bin/zsh
## 自动更换壁纸
echo "eee \
		ddddd"
while ((1)) {
		find ~/Pictures/wallpaper -type f \( -name '*\.jpg' -o -name '*\.png' \) -print0 | shuf -n1 -z | xargs -o feh --bg-scale
		sleep 15m
				
}
