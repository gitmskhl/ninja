import pygame
import sys

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 480
        pygame.display.set_caption('Ninja game')
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.display = pygame.Surface((300, 240))
        # Clock configuration
        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'), 
            'player': load_image('entities/player.png')
        }

        self.movement = [False] * 2
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))
        self.tilemap = Tilemap(self)

    def run(self):
        while True:
            self.display.fill((14, 219, 248))
            self.clock.tick(self.FPS)
            
            self.tilemap.render(self.display)
            self.player.update(((self.movement[1] - self.movement[0]) * 5, 0))
            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, (600, 480)), (0, 0))
            pygame.display.update()


Game().run()