#!/bin/bash
#
# chkconfig: 35 90 12
# description: usbuirtd server
#

# Get function from functions library
#. /etc/init.d/functions

DAEMON_PATH="/some/path/usbuirtd"

# Start
start() {
        ${DAEMON_PATH}/usbuirtd.py start &
        ### Create the lock file ###
        touch /var/lock/subsys/usbuirtd
}

# Stop
stop() {
        ${DAEMON_PATH}/usbuirtd.py stop
        ### Now, delete the lock file ###
        rm -f /var/lock/subsys/usbuirtd
}

case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  status)
        #nothing yet
        ;;
  restart|reload)
        stop
        start
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|reload|status}"
        exit 1
esac

exit 0
