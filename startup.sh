#!/bin/bash
echo "[$(date)] Started"
/home/pi/Discord/ReeeeMan/index.js &
pid[0]=$!
echo "[$(date)] Node server started [PID = ${pid[1]}]"
sleep 2
/home/pi/Discord/ReeeeMan/bot.py &
pid[1]=$!
echo "[$(date)] Python bot started [PID = ${pid[0]}]"
trap "kill ${pid[0]}; kill ${pid[1]}; echo stopped; exit 1" INT EXIT
wait