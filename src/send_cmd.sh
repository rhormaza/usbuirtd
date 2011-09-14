#!/bin/bash

#VARS
DEF_REMOTE="samsung"
DEF_CMD="mute"
DEF_HOST="localhost"
DEF_PORT="8765"

CMD=${1:-$DEF_CMD}
REMOTE=${2:-$DEF_REMOTE}
HOST=${3:-$DEF_HOST}
PORT=${4:-$DEF_PORT}

#BINARIES
ECHO="/bin/echo"
NC="/usr/bin/nc"


$ECHO "${REMOTE} ${CMD}" | $NC $HOST $PORT 
