import pygame
import socket
# import os
# os.environ['SDL_VIDEODRIVER']='windib'
FPS = 60

clientSocket = socket.socket()
clientSocket.connect(('127.0.0.1',7668))
print(clientSocket.recv(1024).decode())

pygame.init()
framesPerSec = pygame.time.Clock()
screen = pygame.display.set_mode((400,500))
screen.fill(pygame.BLACK)
while True:
    keys_pressed = pygame.key.get_pressed()
    if(keys_pressed[pygame.K_UP]):
        clientSocket.send('U'.encode())
    elif(keys_pressed[pygame.K_DOWN]):
        clientSocket.send('D'.encode())
    else:
        clientSocket.send('#'.encode())

    print(f'{clientSocket.recv(1024).decode()}\r')
    framesPerSec.tick(FPS)
    pygame.display.update()