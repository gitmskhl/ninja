import random

class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth
    
    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset=(0, 0)):
        render_pos = [self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth]
        width, height = surf.get_width(), surf.get_height()
        delta_x = self.img.get_width()
        delta_y = self.img.get_height()
        render_pos[0] %= (width + 2 * delta_x)
        render_pos[0] -= delta_x

        render_pos[1] %= (height + 2 * delta_y)
        render_pos[1] -= delta_y

        surf.blit(self.img, render_pos)


class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = []

        for i in range(count):
            cloud = Cloud(
                pos=(random.random() * 999999, random.random() * 999999),
                img=random.choice(cloud_images),
                speed=random.random() * .05 + .05,
                depth=random.random() * .6 + .2
            )
            self.clouds.append(cloud)
        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()
    
    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)