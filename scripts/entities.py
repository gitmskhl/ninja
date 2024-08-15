import pygame
from scripts.utils import AnimationStates

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.max_y_velocity = 5
        self.gravity = .1
        self.anim_offset = ()
        self.flip = False


        states = ['idle', 'run', 'jump', 'slide', 'wall_slide']
        self.animations = AnimationStates(
            animations=[self.game.assets[f'player/{state}'].copy() for state in states],
            states=states,
            firstState='idle'
        )

    def rect(self):
        return pygame.Rect(*self.pos, *self.size)

    def update(self, tilemap, movement=(0, 0)):
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1]
        )

        self.collisions = {'left': False, 'right': False, 'up': False, 'down': False}

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                else:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
                self.velocity[0] = 0
        
        if movement[0] < 0:
            self.flip = True
        if movement[0] > 0:
            self.flip = False
        
        
        self.pos[1] += frame_movement[1]
        self.velocity[1] = min(self.max_y_velocity, self.velocity[1] + self.gravity)
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                else:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
                self.velocity[1] = 0

        self.animations.update()



    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animations.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))



class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
        
        if self.air_time > 4:
            self.animations.set_state('jump')
        elif movement[0] != 0:
            self.animations.set_state('run')
        else:
            self.animations.set_state('idle')