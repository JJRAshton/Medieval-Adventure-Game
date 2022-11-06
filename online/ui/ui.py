import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from api import api

import pygame
pygame.init()

WIDTH = 800
HEIGHT = 600

FPS = 30

def main():
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption('DnD')
    server = api.DNDServer()
    # server.moveRequest(None)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()
        CLOCK.tick(FPS)
    

if __name__ == '__main__':
    main()