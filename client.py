import pygame
import socket
import time
# import os
# os.environ['SDL_VIDEODRIVER']='windib'
FPS = 60
BLACK = (0,0,0)
WHITE = (128,128,128)
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 120
SCREEN_WIDTH = 572 * 2
SCREEN_HEIGHT = 256 * 2
BALL_WIDTH = 12
BALL_HEIGHT = 12

clientSocket = socket.socket()
clientSocket.connect(('127.0.0.1',7668))
gamePort = int(clientSocket.recv(1024).decode())
print(gamePort)
clientSocket.close()

time.sleep(3)
gameSocket = socket.socket()
gameSocket.connect(('127.0.0.1',gamePort))
print(gameSocket.recv(1024).decode())

pygame.init()
framesPerSec = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

while True:
    framesPerSec.tick(FPS)
    screen.fill(BLACK)
    keys_pressed = pygame.key.get_pressed()
    if(keys_pressed[pygame.K_UP]):
        msg = 'U'
        # clientSocket.send('U'.encode())
    elif(keys_pressed[pygame.K_DOWN]):
        msg = 'D'
        # clientSocket.send('D'.encode())
    elif(keys_pressed[pygame.K_q]):
        msg = 'Q'
    else:
        msg = '#'
    
    try:
        gameSocket.send(msg.encode())
    except BrokenPipeError:
        break

    serverResponse = gameSocket.recv(1024).decode()
    p1x,p1y,p2x,p2y,ballx,bally = serverResponse.split(',')

    pygame.draw.rect(screen, WHITE, pygame.Rect(int(p1x),int(p1y), PADDLE_WIDTH,PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, pygame.Rect(int(p2x),int(p2y), PADDLE_WIDTH,PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, pygame.Rect(int(ballx),int(bally), 20,20))

    # time.sleep(0.01)
    pygame.display.update()
    pygame.event.pump()

pygame.quit()
gameSocket.close()