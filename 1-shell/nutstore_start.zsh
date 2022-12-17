#!/bin/zsh

os-info() {
cat /etc/issue | cut -d " " -f 1
}

nutstore-daemon () {
		case $(os-info) {
				("Arch")
					exec nutstore &
					;;
				("Ubuntu")
					${HOME}/.nutstore/dist/bin/nutstore-pydaemon.py &
					;;
}
}

nutstore_daemon() {
params=($*)
if [[ ${params[(i)\-\-force]} -lt $# ]] {
	fparamIndex=${params[(i)\-\-force]}
} elif [[ ${params[(i)\-f]} -lt $# ]] {
	fparamIndex=${params[(i)\-f]}
}

if [[ ${fparamIndex} -lt $# ]] {
case ${params[$(($fparamIndex+1))]} {
("client")
		nutstore-daemon
;;
("web")
	firefox "https://jianguoyun.com/d/home#/" --detach &
;;
}
}
}

