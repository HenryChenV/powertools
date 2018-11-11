#!/bin/sh

#
# 同步电子书到移动硬盘的脚本
#

DIST_DIR="/Volumes/Fun/Ebooks/"

# EMBP
# SRC_DIR="/Users/henry/projects/henry/MyEbooks/"
# MBP
SRC_DIR="/Users/henry/ebook"

# 远程端口
SSH_PORT=22
SSH_USER="henry"
SSH_HOST="192.168.2.15"

RSYNC_OPTIONS="--cvs-exclude --include=*.css -P -rvzc"


rsync_local() {
    echo "Local Mode";
    rsync ${RSYNC_OPTIONS} ${SRC_DIR}/* ${DIST_DIR};
}


rsync_remote() {
    echo "Remote Mode";
    rsync -e "ssh -p ${SSH_PORT}" ${RSYNC_OPTIONS} ${SRC_DIR}/* ${SSH_USER}@${SSH_HOST}:${DIST_DIR}
}

echo_options() {
    echo "################## OPTIONS: #####################"

    echo "SRC_DIR=${SRC_DIR}"
    echo "DIST_DIR=${DIST_DIR}"
    echo

    echo "SSH_PORT=${SSH_PORT}"
    echo "SSH_USER=${SSH_USER}"
    echo "SSH_HOST=${SSH_HOST}"
    echo

    echo "RSYNC_OPTIONS=${RSYNC_OPTIONS}"
    echo

    echo "#################################################"
}


test_ssh_host() {
    echo "Test SSH_HOST[${SSH_HOST}]"

    ping -c 3 ${SSH_HOST}
    RETVAL=$?

    echo "Result is ${RETVAL}"
    echo

    return $RETVAL
}


main() {
    echo_options
    echo

    echo "Rsync Starting..";
    echo

    test_ssh_host
    if [ $? -eq 0 ]; then
        rsync_remote
    else
        rsync_local
    fi

    echo "Rsync End ^-^";
    echo;
}


main


