#!/usr/bin/env bash

ROOTDIR=$(pwd)/$(dirname $0)

$ROOTDIR/daemon.sh restart
