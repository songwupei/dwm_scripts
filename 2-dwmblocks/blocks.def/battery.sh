#!/bin/sh
## use nf-mdi-* font by www.nerdfonts.com/cheat-sheet
ICONbn="" # icon for normal battery
ICONan="" # icon for normal battery
ICONbc="" # icon for critical battery
read -r capacity </sys/class/power_supply/BAT0/capacity
read -r ac </sys/class/power_supply/ADP0/online

crit=15 # critical power_percent
if [ "$ac" = 1 ] ; then 
    printf "电源$ICONan%s%%" "$capacity"
elif  [ "$capacity" -lt "$crit" ] ; then 
		printf "低电$ICONbc%s%%" "$capacity"
		notify-send "请及时插入AC电源充电。"
else
		printf "电池$ICONbn%s%%" "$capacity"
fi
