#!/bin/sh

for i in $(seq 0 3); do
    nitrogen --head=$i --set-zoom --random ~/wallpaper 2> /dev/null &
    sleep 0.5
done
