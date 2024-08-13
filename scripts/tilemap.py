class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = {}

        for i in range(10):
            self.tilemap[str(3 + i) + ";10"] = {
                'type': 'grass',
                'variant': 1,
                'pos': (3 + i, 10)
            }
            self.tilemap["10;" + str(5 + i)] = {
                'type': 'stone',
                'variant': 1,
                'pos': (10, 5 + i)
            }

    def render(self, surf):
        for loc, tile in self.tilemap.items():
            x = int(tile['pos'][0]) * self.tile_size
            y = int(tile['pos'][1]) * self.tile_size
            surf.blit(self.game.assets[tile['type']][tile['variant']], (x, y))

        for loc, tile in self.offgrid_tiles.items():
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])
