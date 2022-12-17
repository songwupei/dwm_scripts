#!/bin/sh
## use nf-mdi-* font by www.nerdfonts.com/cheat-sheet
ICONn="" # icon for normal battery
ICONc="" # icon for critical battery
read -r capacity </sys/class/power_supply/BAT0/capacity
printf "电池$ICONn%s%%" "$capacity"

crit=15 # critical power_percent

if [ "$capacity" -lt "$crit" ] ; then 
		printf "充电$ICONc%s%%" "$capacity"
		notify-send "请及时插入AC电源充电。"
else
		# printf "充电$ICONn%s%%" "$capacity"
		# notify-send "good"
fi
