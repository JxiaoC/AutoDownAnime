#!/bin/bash

#PYTHON_ENV="/home/yada/dandan/bin/activate"
#PYTHON_ENV="python3.6"

usage="Usage: $0 [start | stop]"

PORT_RANGE="10000 10000"
service="auto-down-anime-server"
LOG_DIR="/tmp/androidesk/$service"
pid="$LOG_DIR/service.pid"
log="$LOG_DIR/service.log"


ROOTDIR=$(dirname $0)
MAIN=$ROOTDIR/main.py


if [ ! -d $LOG_DIR ]; then
    mkdir -p "$LOG_DIR"
fi

case $1 in
    (start)

        for i in `seq $PORT_RANGE`
        do
            _pid=$pid.$i
            if [ -f $_pid ]; then
                if kill -0 `cat $_pid` > /dev/null 2>&1; then
                    echo $service running as process `cat $_pid`. Stop it first.
                    exit 1
                fi
            fi

            echo [port: $i] starting $service ...

            nohup python3 $MAIN --port=$i >"$log.$i" 2>&1 < /dev/null &
            echo $! > "$_pid"
            sleep 0.5; head "$log.$i"
        done
        ;;

    (stop)

        for i in `seq $PORT_RANGE`
        do
            _pid=$pid.$i
            if [ -f $_pid ]; then
                if kill -0 `cat $_pid` > /dev/null 2>&1; then
                    echo [port: $i] stopping $service `cat $_pid`...
                    kill `cat $_pid`
                else
                    echo no $service to stop
                fi
            else
                echo no $service to stop
            fi
        done
        ps aux | grep auto_ref_ep.py | awk {'print $2'} | xargs sudo kill -9
        ps aux | grep auto_download.py | awk {'print $2'} | xargs sudo kill -9
        ;;

    (restart)
        ps aux | grep auto_ref_ep.py | awk {'print $2'} | xargs sudo kill -9
        ps aux | grep auto_download.py | awk {'print $2'} | xargs sudo kill -9

        for i in `seq $PORT_RANGE`
        do
            _pid=$pid.$i
            if [ -f $_pid ]; then
                if kill -0 `cat $_pid` > /dev/null 2>&1; then
                    echo [port: $i] stopping $service `cat $_pid`...
                    kill `cat $_pid`
                else
                    echo no $service to stop
                fi
            else
                echo no $service to stop
            fi

            echo [port: $i] starting $service ...

            nohup python3 $MAIN --port=$i >"$log.$i" 2>&1 < /dev/null &
            echo $! > "$_pid"
            sleep 0.5; head "$log.$i"
        done
        ;;

    (test)

        python3 $MAIN --port=9000
        ;;

    (*)
        echo $usage
        exit 1
        ;;

esac
