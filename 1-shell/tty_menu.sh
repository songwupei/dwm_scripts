# Display a Menu
while true
do
    clear
    echo "                  *************************************************"
    echo "                  *                 ArchLinux                     *"
    echo "                  *            Select Windows Manager             *"
    echo "                  *                    SXY                        *"
    echo "                  *************************************************"
    echo
    echo
    echo
    echo
    echo "Select Windows Manager"
    echo "请根据下面的提示选择操作"
    echo
    echo "1) Hyprland"
    echo
    echo
    echo "99) Exit"
    echo "99) 退出"
    echo "Input:"
    echo "输入操作选择: "
        >/dev/null
    read CHOICE
    case "$CHOICE" in
#        1) echo "start DWM... "
#                       exec startx &> /dev/null;
#                       sleep 5;
#                       echo " 回车继续......";
#                        read anykey;;
        1) echo "start Hyprland..."
                        exec Hyprland &> /dev/null;
                         echo "stop end";
                         read anykey;;
        99) exit;;
        *) echo "Please try again!!!"
                        echo "Press Space.....";
                        read anykey;;
    esac
done
