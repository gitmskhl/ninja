import pygame


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.max_y_velocity = 5
        self.gravity = .1

    def rect(self):
        return pygame.Rect(*self.pos, *self.size)

    def update(self, tilemap, movement=(0, 0)):
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1]
        )
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                else:
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x
                self.velocity[0] = 0

        self.pos[1] += frame_movement[1]
        self.velocity[1] = min(self.max_y_velocity, self.velocity[1] + self.gravity)
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                else:
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y
                self.velocity[1] = 0

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
