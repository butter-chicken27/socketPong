import socket 
import pygame

serverSocket = socket.socket()
port = 7668

serverSocket.bind(('', port))        
print ("socket binded to %s" %(port))
serverSocket.listen(2)    
print ("socket is listening")
count = 0
while count < 2:
    if count == 0:
        connection1, add1 = serverSocket.accept()
        count += 1
    else:
        connection2, add2 = serverSocket.accept()
        count += 1
msg1 = "You are player1.\n You play with the left paddle.\n Move with arrows"
connection1.send(msg1.encode())
msg2 = "You are player2.\n You play with the right paddle.\n Move with arrows"
connection2.send(msg2.encode())
connection1.close()
connection2.close()