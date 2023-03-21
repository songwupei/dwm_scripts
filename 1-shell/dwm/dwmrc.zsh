
# slock
## 设置锁屏，并使用slock
## slock 快捷键为win(Mod4)+l
xset s 300 &
${HOME}/.config/dwm/xsidle.sh slock & 

# if connect the Personal  hotspot,open the nutstore web
# else exec nutstore-daemon.py
exec nutstore &
${HOME}/scripts/1-shell/networktool.zsh
# source networktool.zsh
essid=$(getessid) 
essid_deny=("HUAWEIP40" "goood")
## transparent
exec picom &
## notify-send
exec dunst &

/home/song/scripts/2-dwmblocks/daemons/pulse_daemon.sh &
exec dwmblocks &
exec scroll &
sh -c 'xinput --set-button-map "Logitech Wireless Mouse PID:4091" 3 2 1'
## start TLP
sudo tlp start
sudo systemctl mask systemd-rfkill.service

## start netowrk-manager-applet
exec nm-applet &
