#!/bin/bash
datum=date
echo "[$datum] - Started"
/home/pi/Discord/ReeeeMan/index.js &
pid[0]=$!
/home/pi/Discord/ReeeeMan/bot.py &
pid[1]=$!
echo "python pid: ${pid[1]} node pid: ${pid[0]}"
trap "kill ${pid[0]}; kill ${pid[1]}; echo stopped; exit 1" INT EXIT
wait