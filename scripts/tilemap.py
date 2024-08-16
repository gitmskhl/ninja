import pygame

NEIGHBOR_OFFSET = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def render(self, surf, offset=(0, 0)):
        for x in range(
            offset[0] // self.tile_size - 1,
            (surf.get_width() + offset[0]) // self.tile_size + 2
        ):
            for y in range(
                offset[1] // self.tile_size - 1,
                (surf.get_height() + offset[1]) // self.tile_size + 2
            ):
                key=f"{x};{y}"
                if key in self.tilemap:
                    tile = self.tilemap[key]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (x * self.tile_size - offset[0], y * self.tile_size - offset[1]))
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                r = pygame.Rect(
                    tile['pos'][0] * self.tile_size,
                    tile['pos'][1] * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                rects.append(r)
        return rects
    
