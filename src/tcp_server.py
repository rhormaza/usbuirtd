'''
Created on Apr 19, 2011

@author: Raul Hormazabal
'''
__author__  = "rhormaza@gmail.com"
__version__ = "0.0.1"

# TCP server example
import socket
import select
import time
import threading
import traceback
import struct

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
            util.log.debug('device ' + util.CONF_VAR['DEV_FILE'] + ' succesfully opened!')
        except:
            exit('device ' + util.CONF_VAR['DEV_FILE'] + ' has been found')

    def sendIR(self, code):
        #Locking the device /dev/ttyUSBX
        self.lock.acquire()
        util.log.debug('sending cmd through sendIR() method and code:' + code)
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
                time.sleep(float(util.TV_VAR['POWER_DELAY'])) #0.4 or 0.5 couldbe minimun time
                j = 3
                while j > 0:
                    #Locking the device /dev/ttyUSBXX
                    self.lock.acquire()
                    util.log.debug(str(j) + '--> sending cmd' + self.cmd + ' through thread() method')
                    #opening device where usbuirt is hooked up
                    self.usbuirt.transmitIR(util.REMOTE['special'][self.cmd], IRFMT_PRONTO, 1 ,0)
                    self.lock.release()
                    j -= 1
                self.run_thread = False
            time.sleep(0.3)



class TCPServer:
    def __init__(self):
        #list with the open sockets
        open_sockets = []

        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listening_socket.bind(('', util.CONF_VAR['TCP_PORT']))
        listening_socket.listen(util.CONF_VAR['TCP_CLIENT_LISTEN'])

        if util.CONF_VAR['LOG_LEVEL'] != 10:
            util.log.info('*********************************************************')
            util.log.info('*                        NEW LOG                        *')
            util.log.info('*********************************************************')
            
        util.log.info(util.CONF_VAR['APP_NAME']+': starting TCP Server is listening on port ' + str(util.CONF_VAR['TCP_PORT']))
        
        """
        SO_LINGER option is need in order to close the TCP connection
        immediately. Without this, TCP will go to TCP_WAIT state holding
        the socket until timeout. When many connection are done, this is
        something that doesn't look nice :-)
        Also, as we are creating a connection per command, we could
        close the TCP connection immediately without produce any problem. 
        """
        l_onoff = 1                                                                                                                                                           
        l_linger = 0                                                                                                                                                          
        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,                                                                                                                     
                                    struct.pack('ii', l_onoff, l_linger))
#        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 0)
#        listening_socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 5) # set to 60 seconds
#        listening_socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 2) # set to 60 seconds

        #Declaring an instance of UsbUirt class, used to manage usbuirt device
        self._usbuirt = AsynUsbUIRT()
        self._usbuirt.start()
                
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
#                                    util.log.debug(util.REMOTE[remote_name][i]);
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
                        util.log.error('connection closed by peer')
                        socket_to_read.close()
                        open_sockets.remove(socket_to_read)
                        traceback.print_exc()
                        #return []

if __name__ == "__main__":
    TCPServer()
