#!/bin/sh

#conky -c /usr/share/conky/conky_green & disown

while true; do
        echo -e "Select random wallpaper"
        echo -e ""
        ~/bin/change_wallpaper.sh
	sleep 25s
done

