#!/bin/bash
# env-vars
#  . RUNAS_UID  - uid of the user. Eg: $(id -u $USER)
#  . RUNAS_USER - user name of the user Eg: $USER
#  . RUNAS_PRE_SWITCH_CMD - run a command before switching user


echo "Cmd to run: $*"

# this is the case for '-runas user' inside launch script
# create a new user and setup his/her env
if [ "$RUNAS_UID" != "" ] && [ "$RUNAS_USER" != "" ]; then
    echo "Creating env for the user user=$RUNAS_USER uid=$RUNAS_UID"
    export USER=$RUNAS_USER
    export HOME=/home/$USER
    adduser --disabled-password --gecos "" --uid $RUNAS_UID --home $HOME $USER
    mkdir -p /etc/sudoers.d
    echo "$USER ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USER
    chmod 0440 /etc/sudoers.d/$USER
    mkdir -p $HOME
    echo > $HOME/.bashrc
    env | grep -v -e LS_COLORS -e UID >> $HOME/.bashrc
    ldconfig
    if [ "$RUNAS_PRE_SWITCH_CMD" != "" ]; then
        echo "Pre-switch cmd: $RUNAS_PRE_SWITCH_CMD"
        $RUNAS_PRE_SWITCH_CMD
    fi
    exec /opt/runas/exec-as `id -u $USER` `id -g $USER` `pwd` $*
# this is the case for '-runas root' inside launch script
elif [ "$RUNAS_UID" = "" ] && [ "$RUNAS_USER" = "" ]; then
    export USER=root
    export HOME=/$USER
# this is the case for '-runas uid' inside launch script
elif [ "$RUNAS_UID" = "" ] && [ "$RUNAS_USER" != "" ]; then
    export USER=$RUNAS_USER
else
    echo "*ERROR* non-nil RUNAS_UID but nil RUNAS_USER is illegal!"
    exit 1
fi

# This means, either running as root or the docker's "-u" option
# In both cases, just exec!
exec $*
