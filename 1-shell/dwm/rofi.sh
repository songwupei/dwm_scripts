# 打印菜单
call_menu() {
	echo ' set wallpaper'
	echo '艹 update statusbar'
	echo '⎌ set 2monitor'
	echo '⎌ set InnerMonitor'
	echo '⎌ set OutMonitor'
	[ "$(ps aux | grep picom | grep -v 'grep\|rofi\|nvim')" ] && echo ' close picom' || echo ' open picom'
}

# 执行菜单
execute_menu() {
	case $1 in
	' set wallpaper')
		feh --randomize --bg-fill ~/Pictures/wallpaper/*.jpg
		;;
	'艹 update statusbar')
		coproc ($DWM/statusbar/statusbar.sh updateall >/dev/null 2>&1)
		;;
	'⎌ set 2monitor')
		$DWM/set_screen.sh two >/dev/null
		feh --randomize --bg-fill ~/Pictures/wallpaper/*.jpg
		;;
	'⎌ set InnerMonitor')
		exec $DWM/set_screen.sh one >/dev/null
		feh --randomize --bg-fill ~/Pictures/wallpaper/*.jpg
		;;
	'⎌ set OutMonitor')
		exec $DWM/set_screen.sh oneOutMonitor >/dev/null
		feh --randomize --bg-fill ~/Pictures/wallpaper/*.jpg
		;;
		#' open v2raya')
		#  coproc (sudo docker restart v2raya > /dev/null && $DWM/statusbar/statusbar.sh updateall > /dev/null)
		#  ;;
	' close v2raya')
		coproc (sudo docker stop v2raya >/dev/null && $DWM/statusbar/statusbar.sh updateall >/dev/null)
		;;
	' open picom')
		coproc (picom --backend glx --config ~/scripts/config/picom.conf >/dev/null 2>&1)
		;;
	' close picom')
		killall picom
		;;
	esac
}

execute_menu "$(call_menu | rofi -dmenu -p "")"
