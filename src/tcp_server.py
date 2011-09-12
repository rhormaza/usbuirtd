'''
Created on Apr 19, 2011

@author: Raul Hormazabal
'''
# TCP server example
import socket
import select
import time
import threading
import traceback

import util
from usbuirt import UsbUirt
from usbuirt import IRFMT_PRONTO

class AsynUsbUIRT(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.usbuirt = UsbUirt()
        self.run_thread = False
        self.cmd = None
        #this object MUST be open just once through life of the daemon
        try:
            self.usbuirt.open(util.CONF_VAR['DEV_FILE'])
            util.log.info('device ' + util.CONF_VAR['DEV_FILE'] + ' succesfully opened!')
        except:
            exit('device ' + util.CONF_VAR['DEV_FILE'] + ' has been found')

    def sendIR(self, code):
        #Locking the device /dev/ttyUSB0
        self.lock.acquire()
        print '\t 0--> sending cmd through sendIR() method and code:' + code
        #opening device where usbuirt is hooked up
        self.usbuirt.transmitIR(code, IRFMT_PRONTO, 1 ,0)
        time.sleep(0.3)
        self.lock.release()

    def runThread(self, cmd, flag=True):
        self.run_thread = flag
        self.cmd = cmd

    def run(self):
        while True:
            if self.run_thread is True:
                time.sleep(14.3) #0.4 or 0.5 couldbe minimun time
                j = 3
                while j > 0:
                #Locking the device /dev/ttyUSB0
                    self.lock.acquire()
                    print '\t' + str(j) + '--> sending cmd' + self.cmd + ' through thread() method'
                    #opening device where usbuirt is hooked up
                    self.usbuirt.transmitIR(util.REMOTE['special'][self.cmd], IRFMT_PRONTO, 1 ,0)
                    self.lock.release()
                    j -= 1
                self.run_thread = False
            time.sleep(0.3)



class TCPServer:
    def __init__(self):
        #threading.Thread.__init__(self)
        #Declaring an instance of UsbUirt class, used to manage usbuirt device
        #self._usbuirt = AsynUsbUIRT()
        #self._usbuirt.start()
        
        #list with the open sockets
        open_sockets = []

        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listening_socket.bind(('', util.CONF_VAR['TCP_PORT']))
        listening_socket.listen(util.CONF_VAR['TCP_CLIENT_LISTEN'])

        print 'TCPServer Waiting for client on port 8765'
        while True:
            #in this case select() will wait and indicate when data is ready for read
            read_list, write_list, exception_list = select.select([listening_socket] + open_sockets, [], [])
            #iteration over the list of sockets ready for reading
            for socket_to_read in read_list:
                if socket_to_read is listening_socket:
                    #accepting new clients
                    new_socket, address = socket_to_read.accept()
                    util.log.debug('I got a connection from ' +  str(address))
                    open_sockets.append(new_socket)
                else:
                    try:
                        data = socket_to_read.recv(512)
                        data_chunks = data.split();
                        remote_name = data_chunks[0]
                        cmds = data_chunks[1:]
                        ok_counter = 0
                        error_counter = 0
                        for i in cmds:
                            if i in util.REMOTE[remote_name]:
                                if i == 'tv_power_tv' or i == 'tv_power_foxtel' or i == 'tv_power_xbmc':
                                    self._usbuirt.sendIR(util.REMOTE[remote_name]['tv_power_on'])
                                    cmd_to_thread = {
                                      'tv_power_tv': 'tv_tv',
                                      'tv_power_foxtel': 'tv_foxtel',
                                      'tv_power_xbmc': 'tv_xbmc'
                                    }[i]
                                    self._usbuirt.runThread(cmd_to_thread)
                                else:
                                    self._usbuirt.sendIR(util.REMOTE[remote_name][i])

                                time.sleep(0.1)
                                ok_counter += 1
                            else:
                                error_counter += 1
                        if ok_counter > error_counter:
                            socket_to_read.send('ok')
                        else:
                            socket_to_read.send('er')

                        socket_to_read.close()
                        open_sockets.remove(socket_to_read)
                    except :
                        print 'connection closed by peer'
                        socket_to_read.close()
                        open_sockets.remove(socket_to_read)
                        traceback.print_exc()
                        #return []

if __name__ == "__main__":
    TCPServer()
