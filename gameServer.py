import socket 
import pygame
import random
import math
import threading
import time

WHITE = (128, 128, 128)
BLACK = (0, 0, 0)
FPS = 60
SCREEN_WIDTH = 572 * 2
SCREEN_HEIGHT = 256 * 2
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 120
BALL_WIDTH = 12
BALL_HEIGHT = 12

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH,PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT / 2))
    def move(self, key):
        # pressed_key = pygame.key.get_pressed()
        if key == 'U':
            if self.rect.top > 8 * 3:
                self.rect.move_ip(0, -8 * 3)
        if key == 'D':
            if self.rect.bottom < SCREEN_HEIGHT - 8 * 3:
                self.rect.move_ip(0, 8 * 3)

class Ball(pygame.sprite.Sprite):
    speed = 4 * 3
    x_speed = 0
    y_speed = 0
    angle = 0
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_WIDTH,BALL_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.angle = random.uniform(0, 2 * 3.14529)
    def set_speed(self):
        self.speed = 5 * 3
        self.x_speed = 0
        while(abs(self.x_speed) < 10):
            self.angle = random.uniform(0, 2 * 3.14529)
            self.x_speed = self.speed * math.cos(self.angle)
            self.y_speed = self.speed * math.sin(self.angle)
    def move(self):
        if self.y_speed > 0:
            if self.rect.bottom > SCREEN_HEIGHT:
                self.y_speed = self.y_speed * -1
        elif self.y_speed < 0:
            if self.rect.top < 0:
                self.y_speed = self.y_speed * -1
        self.rect.move_ip(self.x_speed, self.y_speed)

def gameRoom(port,availablePorts):
    serverSocket = socket.socket()

    serverSocket.bind(('', port))        
    # print ("socket binded to %s" %(port))
    serverSocket.listen(2)    
    # print ("socket is listening")
    count = 0
    while count < 2:
        if count == 0:
            connection1, add1 = serverSocket.accept()
            count += 1
        else:
            connection2, add2 = serverSocket.accept()
            count += 1
    msg1 = "You are player1.\n You play with the left paddle.\n Move with arrows\n Press Q to quit"
    connection1.send(msg1.encode())
    msg2 = "You are player2.\n You play with the right paddle.\n Move with arrows\n Press Q to quit"
    connection2.send(msg2.encode())

    pygame.init()
    FramesPerSec = pygame.time.Clock()

    P1 = Paddle(45)
    P2 = Paddle(SCREEN_WIDTH - 45)
    ball = Ball()
    ball.set_speed()
    players = pygame.sprite.Group()
    players.add(P1)
    players.add(P2)

    while True:
        msg1 = connection1.recv(1024).decode()
        msg2 = connection2.recv(1024).decode()
        if msg1 == 'Q' or msg2 == 'Q':
            break
        moves = [(P1,msg1),(P2,msg2)]
        for (player,key) in moves:
            player.move(key)
        ball.move()

        if pygame.sprite.spritecollideany(ball,players):
            ball.x_speed *= -1

        if ball.rect.right > SCREEN_WIDTH:
            #Resetting the ball position when a player loses
            ball = Ball()
            ball.set_speed()

        if ball.rect.left < 0:
            #Resetting the ball position when a player loses
            ball = Ball()
            ball.set_speed()

        state = f'{P1.rect[0]},{P1.rect[1]},{P2.rect[0]},{P2.rect[1]},{ball.rect[0]},{ball.rect[1]}'
        connection1.send(state.encode())
        connection2.send(state.encode())
    connection1.close()
    connection2.close()
    serverSocket.close()

    #Waiting for the socket to fully close before actually setting the port to available
    time.sleep(20)
    availablePorts[port - 8000] = True

def main():
    mainPort = 7668
    serverSocket = socket.socket()
    serverSocket.bind(('',mainPort))        
    # print ("socket binded to %s" %(port))
    serverSocket.listen(20)    
    # print ("socket is listening")
    ports = [True for i in range(10)]
    while True:
        count = 0
        while count < 2:
            if count == 0:
                connection1, add1 = serverSocket.accept()
                count += 1
            else:
                connection2, add2 = serverSocket.accept()
                count += 1
        index = 0
        while not ports[index]:
            index += 1
        gamePort = 8000 + index
        ports[index] = False
        connection1.send(str(gamePort).encode())
        connection2.send(str(gamePort).encode())
        gameThread = threading.Thread(target=gameRoom,args=(gamePort,ports))
        gameThread.start()

if __name__ == '__main__':
    main()
