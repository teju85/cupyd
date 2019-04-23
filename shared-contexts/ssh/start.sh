#!/bin/bash
# This handy script is supposed to get called before running any user commands.
# During this time, this script will setup the user password for the ssh login.
# This helps the '-runas user' launch option to work with remote ssh login.
#
# This is sxpected to be run as the RUNAS_PRE_SWITCH_CMD hook.
# Thus, currently, this works only for '-runas user' case.
# In future, support will be tried for '-runas uid' case as well.

echo "Setting up password for user=$USER"
echo "$USER:$USER" | chpasswd
echo "Starting ssh server..."
service ssh stop
service ssh start
