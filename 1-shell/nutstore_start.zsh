#!/bin/zsh
nutstore-daemon() {
				case $(cat /etc/issue | cut -d " " -f1) {
				("Arch")
					exec nutstore &
					;;
				("Ubuntu")
					${HOME}/.nutstore/dist/bin/nutstore-pydaemon.py &
					;;
}
}

