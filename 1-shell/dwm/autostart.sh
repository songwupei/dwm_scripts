#! /bin/bash
# DWM自启动脚本 仅作参考 
# 搭配 https://github.com/yaocccc/scripts 仓库使用 目录位置 ~/scripts
# 部分配置文件在 ~/scripts/config 目录下

_thisdir=$(cd $(dirname $0);pwd)

settings() {
    [ $1 ] && sleep $1
    xset -b                                   # 关闭蜂鸣器
    syndaemon -i 1 -t -K -R -d                # 设置使用键盘时触控板短暂失效
    $DWM/set_screen.sh two               # 设置显示器
}

daemons() {
    [ $1 ] && sleep $1
    $_thisdir/statusbar/statusbar.sh cron &   # 开启状态栏定时更新
    #xss-lock -- ~/scripts/blurlock.sh &       # 开启自动锁屏程序
    #fcitx5 &                                  # 开启输入法
    ibus-daemon --xim -d &                     #better 开启输入法
    #ibus-daemon -rxR &                        # 开启输入法
    nutstore &
    #picom --experimental-backends --config ~/scripts/config/picom.conf >> /dev/null 2>&1 & # 开启picom
    dunst -conf ~/scripts/config/dunst.conf & # 开启通知server
    #lemonade server &                         # 开启lemonade 远程剪切板支持
    flameshot &                               # 截图要跑一个程序在后台 不然无法将截图保存到剪贴板
    picom --backend glx --config ~/scripts/config/picom.conf >> /dev/null 2>&1 & # 开启picom
    xset s 100 &
    $DWM/xsidle.sh slock &
}

cron() {
    [ $1 ] && sleep $1
    let i=1200
    while true; do
        [ $((i % 30)) -eq 0 ] && ~/scripts/set_screen.sh check # 每10秒检查显示器状态 以此自动设置显示器
        [ $((i % 1200)) -eq 0 ] && feh --randomize --bg-fill ~/Pictures/wallpaper/*.jpg # 每300秒更新壁纸
        sleep 1200; let i+=1200
    done
}

settings 4 &                                  # 初始化设置项
daemons 4 &                                   # 后台程序项
cron 4 &                                      # 定时任务项
