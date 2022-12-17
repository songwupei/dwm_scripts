#!/bin/sh
# (for pulseaudio users)
# This script parses the output of `pacmd list-sinks' to find volume and mute
# status of the default audio sink and whether headphones are plugged in or not
# Also see ../daemons/pulse_daemon.sh
## use nf-mdi-* font by www.nerdfonts.com/cheat-sheet
pacmd list-sinks | awk '
    BEGIN {
        ICONsn = "\x0cﱜ\x0b" # headphone unplugged, not muted
        ICONsm = "\x0dﱝ\x0b" # headphone unplugged, muted
        ICONhn = "\x0c \x0b" # headphone plugged in, not muted
        ICONhm = "\x0d \x0b" # headphone plugged in, muted
    }
    f {
        if ($1 == "muted:" && $2 == "yes") {
            m = 1
        } else if ($1 == "volume:") {
            if ($3 == $10) {
                vb = $5
            } else {
                vl = $5
                vr = $12
            }
        } else if ($1 == "active" && $2 == "port:") {
            if (tolower($3) ~ /headphone/)
                h = 1
            exit
        }
        next
    }
    $1 == "*" && $2 == "index:" {
        f = 1
    }
    END {
        if (f) {
            printf "音量%s", h ? (m ? ICONhm : ICONhn) : (m ? ICONsm : ICONsn)
            if (vb)
                print vb
            else
                printf "L%s R%s\n", vl, vr
        }
    }
'
