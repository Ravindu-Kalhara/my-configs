#!/usr/bin/env bash 

numlockx on &
xss-lock --transfer-sleep-lock -- i3lock --nofork &
lxsession &
~/.config/fehbg &
udisksctl mount --block-device /dev/sdb1 >> /dev/null &
pcmanfm -d &

