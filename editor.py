import pygame
import sys

from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0


class Editor:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 480
        pygame.display.set_caption('editor')
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
        }

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.movement = [False] * 4
        self.scroll = [0] * 2

        self.tilemap = Tilemap(self)
        
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

        self.special_keys = {
            'ctrl': False,
            's': False,
            't': False
        }

    def change_tile(self, next, group):
        sign = 2 * next - 1
        if group:
            self.tile_group = (self.tile_group + sign) % len(self.tile_list)
            self.tile_variant = 0
        else:
            self.tile_variant = (self.tile_variant + sign) % len(self.assets[self.tile_list[self.tile_group]])

    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            self.clock.tick(self.FPS)
            
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant]
            
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, offset=render_scroll)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tsize = self.tilemap.tile_size
            tile_pos = (
                int((mpos[0] + self.scroll[0]) // tsize),
                int((mpos[1] + self.scroll[1]) // tsize)
            )
            pos = (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])

            current_tile_img.set_alpha(100)
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * tsize - self.scroll[0] , tile_pos[1] * tsize - self.scroll[1]))
                current_tile_img.set_alpha(255)
                if self.clicking:
                    self.tilemap.tilemap[f"{tile_pos[0]};{tile_pos[1]}"] = {
                        'type': self.tile_list[self.tile_group],
                        'variant': self.tile_variant,
                        'pos': tile_pos
                    }
                
            else:
                self.display.blit(current_tile_img, (mpos[0] , mpos[1]))
                current_tile_img.set_alpha(255)
                if self.clicking:
                    size = self.assets[self.tile_list[self.tile_group]][self.tile_variant].get_size()
                    self.tilemap.offgrid_tiles.append({
                        'type': self.tile_list[self.tile_group],
                        'variant': self.tile_variant,
                        'pos': pos,
                        'rect': (pos[0], pos[1], *size)
                    })
            
            if self.right_clicking:
                if f"{tile_pos[0]};{tile_pos[1]}" in self.tilemap.tilemap:
                    del self.tilemap.tilemap[f"{tile_pos[0]};{tile_pos[1]}"]
                
                for i, tile in enumerate(self.tilemap.offgrid_tiles):
                    if pygame.Rect(*tile['rect']).collidepoint(pos):
                        self.tilemap.offgrid_tiles.pop(i)

            if self.special_keys['ctrl'] and self.special_keys['s']:
                self.tilemap.save('map.json')
            
            if self.special_keys['t']:
                self.tilemap.autotile()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True      
                    if event.button == 3:
                        self.right_clicking = True
                    if event.button in [4, 5]:
                        self.change_tile(event.button == 5, not self.shift)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False   
                    if event.button == 3:
                        self.right_clicking = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_LCTRL:
                        self.special_keys['ctrl'] = True
                    if event.key == pygame.K_s:
                        self.special_keys['s'] = True
                    if event.key == pygame.K_t:
                        self.special_keys['t'] = True
                    
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key in [pygame.K_e, pygame.K_q]:
                        self.change_tile(event.key == pygame.K_e, not self.shift)
                    

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                    if event.key == pygame.K_LCTRL:
                        self.special_keys['ctrl'] = False
                    if event.key == pygame.K_s:
                        self.special_keys['s'] = False
                    if event.key == pygame.K_t:
                        self.special_keys['t'] = False

            self.screen.blit(pygame.transform.scale(self.display, (600, 480)), (0, 0))
            pygame.display.update()


Editor().run()