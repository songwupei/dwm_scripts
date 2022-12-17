#!/bin/zsh
## to get network infos
getessid() {
iwconfig wlp1s0 | grep ESSID: | sed 's/.*ESSID://' | tr -d '"' | tr -d ' '
}
