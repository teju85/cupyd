#!/bin/bash
resolution=${1:-1600x1200}
if [ "$VNC_SETUP" != "1" ]; then
    echo "VNC env is not setup for this image!"
    exit 0
fi
if [ ! -d "$HOME/.vnc" ]; then
    mkdir -p $HOME/.vnc
    touch $HOME/.Xauthority $HOME/.Xresources
    cp /.xinitrc $HOME/.xinitrc
    cp /.xsession $HOME/.xsession
fi
exec x11vnc -display :0 -create -shared -forever -scale $resolution
