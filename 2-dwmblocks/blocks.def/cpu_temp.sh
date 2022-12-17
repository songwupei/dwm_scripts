#!/bin/sh
# nf-mdi-* www.nerdfonts.com/cheat-sheet

ICONn=" " # icon for normal temperatures
ICONc="ﴛ " # icon for critical temperatures

crit=70 # critical temperature

read -r temp </sys/class/thermal/thermal_zone0/temp
temp="${temp%???}"

if [ "$temp" -lt "$crit" ] ; then
    printf "温度$ICONn%s°C" "$temp"
else
	printf "温度$ICONc%s°C" "$temp"
fi
