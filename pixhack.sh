#! /bin/bash

PIXHACK_PATH=`pwd`

os=`uname -s`
if [ $os == "Linux" ]; then
    seq_command='seq'
    ping_cmd="ping -c1 -w2"
    ssh_cmd="ssh -q"
elif [ $os == "Darwin" ]; then
    seq_command='jot -'
    ping_cmd="ping -c1 -W2"
    ssh_cmd="ssh -q"
fi

function start_crawler () {
    echo "[info] start crawling......"
    cd crawler/
    scrapy crawl blog
}

function start_jieba() {
    echo "[info] start jeiba......"
}

function argument_echo ()
{
    echo "[PixHack]
    Usage: `basename $0` {arg}
    --crawler
    --jieba
    "
}

case "$1" in
    --crawler)
        start_crawler
        ;;
    --jieba)
        start_jieba
        ;;
    *)
        argument_echo
        exit 1
        ;;
esac
