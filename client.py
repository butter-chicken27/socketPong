import pygame
import socket

clientSocket = socket.socket()
clientSocket.connect(('192.168.0.6',7669))
print(clientSocket.recv(1024).decode())

pygame.init()
screen = pygame.display.set_mode((400,500))

while True:
    keys_pressed = pygame.key.get_pressed()
    if(keys_pressed[pygame.K_UP]):
        clientSocket.send('U')
    elif(keys_pressed[pygame.K_DOWN]):
        clientSocket.send('D')
    else:
        clientSocket.send('#')

    print(f'{clientSocket.recv(1024).decode()}\r')