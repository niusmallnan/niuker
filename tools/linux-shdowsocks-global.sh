#!/bin/bash

# extern variables
SCRIPT_FULL_NAME=$0
SCRIPT_PID=$$
SCRIPT_PID_FILE=/tmp/shadowsocks_ss.pid
SS=ss-redir
SS_IP=127.0.0.1
SS_PORT=8888
SS_LOCAL_PORT=1080
SS_PASSWORD=xxxxxx
SS_METHOD=chacha20
SS_CONFIG_DIR=/etc/shadowsocks
SS_CONFIG_FILE=${SS_CONFIG_DIR}/shadowsocks.json
SS_OPTIONAL_ARGS=""
CHAIN_NAME=SHADOWSOCKS
VERSION=1.0.1

# root
if [ "$UID" != "0" ]; then
    echo "You must use root priviledge!";
    exit -1;
fi

help() {
    echo "Shadowsocks Global Script"
    echo "         -- Author : Cole Smith"
    echo "         -- Email  : tobewhatwewant@gmail.com"
    echo "Usage:"
    echo "  $0 start|stop|restart"
    echo ""
    echo "Options:"
    echo "   -c, --clear                        Clear Network Configure."
    echo "   -f, --configfile ConfigFilePath    Load Specific Configure File Path."
    echo "   -g, --global                       Load Vps Shadowsocks Configure File."
    echo "   -h, --help                         Get Help."
    echo "   -l, --log                          Stdout Log Infomation."
    echo "   -r, --remove                       Remove Old Config."
    echo "   -u, --update                       Update Lastest Version."
    echo "   -v, --version                      Get Script Version."
}

check_state() {
    if [ -f "$SCRIPT_PID_FILE" ]; then
        echo "Error:"
        echo "    Already start Shadowsocks Global Agent."
        echo "(You can restart it by option restart)"
        exit -1
    fi
}

initialize() {
    # check first
    # initialize_check

    # create pid file
    echo $SCRIPT_PID > $SCRIPT_PID_FILE
}

_cleanup() {
    trap "" SIGINT
    trap "" SIGUSR1

    sudo iptables -t nat -F $CHAIN_NAME
    sudo iptables -t mangle -F $CHAIN_NAME
    sleep 2
    sudo iptables -t nat -D OUTPUT -j $CHAIN_NAME
    sudo iptables -t mangle -D OUTPUT -j $CHAIN_NAME
    #sudo iptables -t nat -D PREROUTING -p tcp -j $CHAIN_NAME
    #sudo iptables -t mangle -D PREROUTING -j $CHAIN_NAME
    sleep 2
    sudo iptables -t nat -X $CHAIN_NAME
    sudo iptables -t mangle -X $CHAIN_NAME

    ip rule del fwmark 0x01/0x01 table 100
    ip route del local 0.0.0.0/0 dev lo table 100
    # delete pid file
    rm -rf $SCRIPT_PID_FILE
}

cleanup() {
    echo
    echo "Cleaning Config..."
    _cleanup > /dev/null 2>&1
    echo "Clean done."
}

clean_exit() {
    cleanup
    exit 0
}

update_lastest_version() {
    ADDR="https://raw.githubusercontent.com/whatwewant/whatwewant.github.io/master/scripts/linux-shdowsocks-global.sh"
    wget $ADDR -O $SCRIPT_FULL_NAME && \
    echo "Succeed in update to the lastest version" || \
    echo "Update Error."
}

# enumerate random
function random ()
{
    min=1503;
    max=65535;
    num=$(date +%s+%N);
    ((retnum=num%max+min));
    # echo $retnum;
    # return $retnum;
    SS_LOCAL_PORT=$retnum;
}

# random SS_PORT
# random;

case $1 in
    -c|--clear)
        cleanup
        exit 0
        ;;
    -h|--help)
        help
        exit 0
        ;;
    -u|--update)
        update_lastest_version
        exit 0
        ;;
    -v|--version)
        echo $VERSION
        exit 0
        ;;
    -r|--remove)
        rm -rf $SS_CONFIG_FILE > /dev/null 2>&1
        echo "Succeed in removing the Old Config File."
        echo ""
        ;;
    start)
        check_state
        ;;
    stop)
        echo "stop now ..."
        if [ ! -f "$SCRIPT_PID_FILE" ]; then
            echo "Shadowsocks Global Agent Never Starts."
            exit -1
        fi
        X_PID=$(cat $SCRIPT_PID_FILE)
        kill $X_PID > /dev/null 2>&1
        killall ss-redir > /dev/null 2>&1
        cleanup
        echo "Stop Successfully."
        exit 0
        ;;
    restart)
        echo "restart now ..."
        rm -rf $SCRIPT_PID_FILE >> /dev/null
        kill $(cat $SCRIPT_PID_FILE) >> /dev/null 2>&1
        killall ss-redir > /dev/null 2>&1
        ;;
    *)
        echo "Unknown Arguments."
        echo "Option -h For help."
        exit -1
        ;;
esac

# Options
case $2 in
    "")
        ;;
    -c|--clear)
        cleanup
        exit 0
        ;;
    -f|--configfile)
        SS_CONFIG_FILE=$3
        ;;
    -g|--global)
        SS_CONFIG_FILE=${SS_CONFIG_DIR}/shadowsocks-vps.json
        ;;
    -h|--help)
        help
        exit 0
        ;;
    -l|--log)
        SS_OPTIONAL_ARGS=$SS_OPTIONAL_ARGS" -v"
        ;;
    -r|--remove)
        rm -rf $SS_CONFIG_FILE > /dev/null 2>&1
        echo "Succeed in removing the Old Config File."
        echo ""
        ;;
    -u|--update)
        update_lastest_version
        exit 0
        ;;
    -v|--version)
        echo $VERSION
        exit 0
        ;;
    *)
        echo "Error:"
        echo "    Unknown Arguments. -h Or --help For Help."
        exit
        ;;
esac


if [ ! -f $SS_CONFIG_FILE ]; then
    echo "First Use, Please Config Shadowsocks:"
    echo -n "Server IP: "
    read SS_IP

    echo -n "Server_PORT: "
    read SS_PORT

    echo -n "LOCAL_PORT(Default: 1503): "
    read SS_LOCAL_PORT
    SS_LOCAL_PORT=${SS_LOCAL_PORT:-1503}
    while [ "$SS_PORT" = "$SS_LOCAL_PORT" ]; 
    do
        echo "Server Port cannot be the same as SS_LOCAL_PORT. Try Again."
        echo -n "LOCAL_PORT: "
        read SS_LOCAL_PORT
    done

    echo -n "Server Password: "
    read SS_PASSWORD

    echo -n "Server Method (Default: aes-256-cfb): "
    read SS_METHOD
    SS_METHOD=${SS_METHOD:-"aes-256-cfb"}
    # if [ "$SS_METHOD" = "" ]; then
    #     SS_METHOD=aes-256-cfb
    # fi

    [[ $SS_IP && $SS_PORT && $SS_LOCAL_PORT && \
        $SS_PASSWORD && $SS_METHOD ]] || \
        (
            echo "" && echo "Error:" && \
            echo "    Each Variables mustn't be Empty Value." && \
            exit -1
        )

    # config shadowsocks
    if [ ! -d "$SS_CONFIG_DIR" ]; then
        mkdir -p $SS_CONFIG_DIR;
    fi

    # save config to $SS_CONFIG_FILE
    echo "{" > $SS_CONFIG_FILE
    echo "  \"server\": \"$SS_IP\"," >> $SS_CONFIG_FILE
    echo "  \"server_port\": $SS_PORT," >> $SS_CONFIG_FILE
    echo "  \"local_port\": $SS_LOCAL_PORT," >> $SS_CONFIG_FILE
    echo "  \"password\": \"$SS_PASSWORD\"," >> $SS_CONFIG_FILE
    echo "  \"method\": \"$SS_METHOD\"" >> $SS_CONFIG_FILE
    echo "}" >> $SS_CONFIG_FILE
    # save end
else
# read config
SS_IP=$(cat $SS_CONFIG_FILE| grep -i server | head -n 1 | awk -F '"' '{print $4}')
SS_PORT=$(cat $SS_CONFIG_FILE| grep -i server_port | head -n 1 | awk -F ' ' '{print $2}' | awk -F ',' '{print $1}')
SS_LOCAL_PORT=$(cat $SS_CONFIG_FILE| grep -i local_port | head -n 1 | awk -F ' ' '{print $2}' | awk -F ',' '{print $1}')
SS_PASSWORD=$(cat $SS_CONFIG_FILE| grep -i password | head -n 1 | awk -F '"' '{print $4}')
SS_METHOD=$(cat $SS_CONFIG_FILE| grep -i method | head -n 1 | awk -F '"' '{print $4}')

# echo config
echo "Use Old Config in $SS_CONFIG_FILE:"
echo "server: $SS_IP"
echo "server_port: $SS_PORT"
echo "local_port: $SS_LOCAL_PORT"
echo "password: ***********"
echo "method: $SS_METHOD"
fi

# iptables
which iptables >> /dev/null;
if [ "$?" != "0" ]; then
    echo "Please install iptables first."
    exit -1
fi

# shadowsocks
which $SS >> /dev/null
if [ "$?" != "0" ]; then
    echo "Please install shadowsocks-libev first."
    echo "What we need is ss-redir"
    exit -1
fi

# catch ctrl+c to start clean_exit function
trap "clean_exit" SIGINT
trap "clean_exit" SIGUSR1

# initialize data
initialize

# iptables
sudo iptables -t nat -L $CHAIN_NAME >> /dev/null 2>&1
if [ "$?" != "0" ]; then
    sudo iptables -t nat -N $CHAIN_NAME
    sleep 3
fi
sudo iptables -t nat -F

sudo iptables -t mangle -L $CHAIN_NAME >> /dev/null 2>&1
if [ "$?" != "0" ]; then
    sudo iptables -t mangle -N $CHAIN_NAME
    sleep 3
fi
sudo iptables -t mangle -F


## iptables Ignore shadowsocks address
sudo iptables -t nat -A $CHAIN_NAME -d $SS_IP -j RETURN

## Ignore LANs and any other addresses you'd like to bypass the proxy
sudo iptables -t nat -A $CHAIN_NAME -d 0.0.0.0/8 -j RETURN
sudo iptables -t nat -A $CHAIN_NAME -d 10.0.0.0/8 -j RETURN
sudo iptables -t nat -A $CHAIN_NAME -d 127.0.0.0/8 -j RETURN
sudo iptables -t nat -A $CHAIN_NAME -d 169.254.0.0/16 -j RETURN
#sudo iptables -t nat -A $CHAIN_NAME -d 172.16.0.0/12 -j RETURN
#sudo iptables -t nat -A $CHAIN_NAME -d 172.17.0.0/16 -j RETURN
sudo iptables -t nat -A $CHAIN_NAME -d 192.168.0.0/16 -j RETURN
sudo iptables -t nat -A $CHAIN_NAME -d 224.0.0.0/4 -j RETURN
sudo iptables -t nat -A $CHAIN_NAME -d 240.0.0.0/4 -j RETURN

## Anything else should be redirected to shadowsocks's local port
sudo iptables -t nat -A $CHAIN_NAME -p tcp -j REDIRECT --to-ports $SS_LOCAL_PORT
#sudo iptables -t nat -A $CHAIN_NAME -p udp -j REDIRECT --to-ports $SS_LOCAL_PORT
#sudo iptables -t nat -A $CHAIN_NAME -p icmp -j REDIRECT --to-ports $SS_LOCAL_PORT

# Add any UDP rules
sudo ip rule add fwmark 0x01/0x01 table 100
sudo ip route add local 0.0.0.0/0 dev lo table 100
sudo iptables -t mangle -A $CHAIN_NAME -p udp --dport 53 -j TPROXY --on-port $SS_LOCAL_PORT --tproxy-mark 0x01/0x01

# Apply the rules
sudo iptables -t nat -L OUTPUT | grep $CHAIN_NAME >> /dev/null
if [ "$?" != "0" ]; then
    sudo iptables -t nat -I OUTPUT -j $CHAIN_NAME
fi
sudo iptables -t mangle -L OUTPUT | grep $CHAIN_NAME >> /dev/null
if [ "$?" != "0" ]; then
    sudo iptables -t mangle -I OUTPUT -j $CHAIN_NAME
fi

#sudo iptables -t nat -A PREROUTING -p tcp -j $CHAIN_NAME
#sudo iptables -t mangle -A PREROUTING -j $CHAIN_NAME

## SAVE iptables config
sudo iptables-save >> /dev/null

# Start the shadowsocks-redir
# if [ "$1" == "-d" ]; then
#    echo "Shadowsocks Daemon Now."
#    $SS -c $SS_CONFIG_FILE -f /tmp/shadowsocks.pid
#else
echo "Start shadowsocks redirect ..."
$SS -u -v -c $SS_CONFIG_FILE $SS_OPTIONAL_ARGS
#fi
