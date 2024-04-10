import pygame
from pygame import Rect, Vector2
from pygame.sprite import Group, Sprite

from sonar.const import black


class Wall(pygame.sprite.Sprite):
    def __init__(self, rect: Rect, group: Group):
        super().__init__(group)
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        # self.image.fill('white')
        self.image.fill(black)


class Walls(pygame.sprite.Group):
    def __init__(self, surface, tmx_layer, cell_size):
        # self.color = (0, 0, 0, 0)
        super().__init__()
        self.surface = surface
        self.walls = []
        self.grid_cell_size = cell_size
        self.tmx_layer = tmx_layer
        self.tiles = []
        self.get_tiles_from_tmx()
        self.get_merged_walls_y()
        print(len(self.tiles))
        print(len(self.sprites()))
        print(len(self.walls))


    # def get_walls_from_tmx(self):
    #     for obj in self.tmx_layer.objects:
    #         if obj.type != 'marker':
    #             wall = Wall(pygame.Rect(obj.x, obj.y, obj.width, obj.height), self)
    #             self.walls.append(wall)

    def get_tiles_from_tmx(self):
        for x, y, surf in self.tmx_layer.tiles():
            pos = (x * self.grid_cell_size, y * self.grid_cell_size)
            rect = pygame.Rect(pos, (self.grid_cell_size, self.grid_cell_size))
            self.tiles.append(rect)

    def get_nearby_walls(self, pos, radius):
        nearby_walls = Group()
        nearby_walls.add([wall for wall in self.walls if Vector2(wall.rect.center).distance_to(Vector2(pos)) <= radius])
        return nearby_walls

    def get_merged_walls_y(self):
        merged_tiles = []
        for i in range(len(self.tiles)):
            if self.tiles[i] in merged_tiles:
                continue

            next_offset = 20
            current_rect = [self.tiles[i]]

            for j in range(len(self.tiles)):
                next_square_nearby = self.tiles[i].y + next_offset == self.tiles[j].y and self.tiles[i].x == self.tiles[j].x
                if next_square_nearby:
                    current_rect.append(self.tiles[j])
                    merged_tiles.append(self.tiles[j])
                    next_offset += 20

            merged_rect = Rect(current_rect[0].x, current_rect[0].y, 20, len(current_rect) * 20)
            self.walls.append(Wall(merged_rect, self))
            current_rect.clear()


class Marker(pygame.sprite.Sprite):
    def __init__(self, rect: Rect, group: Group):
        super().__init__(group)
        self.rect = rect
        self.frames = []
        self.load_frames()
        self.anim_index = 0
        self.image = self.frames[self.anim_index]

    def load_frames(self):
        for i in range(1, 7):
            image = pygame.image.load(f'res/animated_sprite/marker/{i}.png').convert_alpha()
            smaller_image = pygame.transform.smoothscale(image, (35, 35))
            self.frames.append(smaller_image)

    def on_collide(self, player):
        if pygame.sprite.collide_rect(player, self):
            pass
            # TODO on collide

    def proceed_animation(self):
        self.anim_index += 0.12
        if self.anim_index > len(self.frames):
            self.anim_index = 0

        self.image = self.frames[int(self.anim_index)]

    def update(self, player):
        self.proceed_animation()
        self.on_collide(player)


class Markers(pygame.sprite.Group):
    def __init__(self, surface, tmx_layer, player: Sprite):
        super().__init__()
        self.surface = surface
        self.player = player

        self.tmx_layer = tmx_layer
        self.get_markers_from_tmx()

    def get_markers_from_tmx(self):
        for obj in self.tmx_layer:
            if obj.type == 'marker':
                Marker(pygame.Rect(obj.x, obj.y, obj.width, obj.height), self)
