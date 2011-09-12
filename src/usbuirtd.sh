#!/bin/bash
#
# chkconfig: 35 90 12
# description: Foo server
#

# Get function from functions library
#. /etc/init.d/functions

# Start the service FOO
start() {
        /home/xbmc/CoreData/UsbUIRT/usbuirtd.py start &
        ### Create the lock file ###
        touch /var/lock/subsys/usbuirtd
}

# Restart the service FOO
stop() {
        #killproc FOO
        /home/xbmc/CoreData/UsbUIRT/usbuirtd.py
        ### Now, delete the lock file ###
        rm -f /var/lock/subsys/usbuirtd
}

### main logic ###
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  status)
        #status FOO
        ;;
  restart|reload|condrestart)
        stop
        start
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|reload|status}"
        exit 1
esac

exit 0
