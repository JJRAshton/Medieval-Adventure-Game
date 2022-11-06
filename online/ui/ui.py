import pygame
import api
pygame.init()

WIDTH = 800
HEIGHT = 600

FPS = 30

def main():
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption('DnD')
    server = api.DNDServer()

    while True:
        CLOCK.tick(FPS)
    

if __name__ == '__main__':
    main()