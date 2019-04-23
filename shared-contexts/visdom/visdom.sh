#!/bin/bash
# script to setup visdom env and start sever in the background
# Usage: visdom.sh <visdomPort>
port=${VISPORT:-8097}
level=${1:-WARN}
pid=`ps aux | grep visdom.server | grep -v 'grep visdom.server'`
if [ "$pid" != "" ]; then
    echo "visdom server already running..."
    echo "  $pid"
else
    echo "Starting visdom server..."
    python3 -m visdom.server -port $port -logging_level $level &
fi
