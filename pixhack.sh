#! /bin/bash

export PIXHACK_PATH=`pwd`
export PYTHONPATH="${PYTHONPATH}":$PIXHACK_PATH
export SQL_PATH=$PIXHACK_PATH/sql

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
    python $PIXHACK_PATH/jieba/Jieba.py
}

function start_test() {
    echo "[info] start testing......"
    for file in $PIXHACK_PATH/crawler/pixnet/test/*.py
    do
        python $file
    done

}

function argument_echo ()
{
    echo "[PixHack]
    Usage: `basename $0` {arg}
    --crawler
    --jieba
    --test
    "
}

case "$1" in
    --crawler)
        start_crawler
        ;;
    --jieba)
        start_jieba
        ;;
    --test)
        start_test
        ;;
    *)
        argument_echo
        exit 1
        ;;
esac
