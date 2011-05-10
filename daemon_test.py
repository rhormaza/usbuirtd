'''
Created on Apr 21, 2011

@author: wired
'''

import sys, time
from daemon import Daemon
from tcp_server import TCPServer

class MyDaemon(Daemon):
    def run(self):
        TCPServer()
#        while True:
#            time.sleep(1)
#            f = open('/dev/ttys001','w')
#            f.write('running....\r\n')
#            f.flush()
#            f.close()

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
