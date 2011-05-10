'''
Created on Apr 19, 2011

@author: Raul Hormazabal
'''
# TCP client example
import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 5000))
while 1:
    data = raw_input ("SEND( TYPE q or Q to Quit):") 
    if (data <> 'Q' and data <> 'q'):
        client_socket.send(data)
        print 'output: ' + str(client_socket.recv(512))
    else:
        client_socket.send(data)
        print 'output: ' + str(client_socket.recv(512))
        time.sleep(1)
        client_socket.close()
        break

            
