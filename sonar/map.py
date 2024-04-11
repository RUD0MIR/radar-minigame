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
        self.get_merged_walls()
        print(f"tiles: {len(self.tiles)}")
        print(f"sprites: {len(self.sprites())}")
        print(f"walls: {len(self.walls)}")

    def get_tiles_from_tmx(self):
        for x, y, surf in self.tmx_layer.tiles():
            pos = (x * self.grid_cell_size, y * self.grid_cell_size)
            rect = pygame.Rect(pos, (self.grid_cell_size, self.grid_cell_size))
            self.tiles.append(rect)

    def get_walls_from_tmx(self):
        for obj in self.tmx_layer.objects:
            if obj.type != 'marker':
                wall = Wall(pygame.Rect(obj.x, obj.y, obj.width, obj.height), self)
                self.walls.append(wall)

    def get_nearby_walls(self, pos, radius):
        nearby_walls = Group()
        nearby_walls.add([wall for wall in self.walls if Vector2(wall.rect.center).distance_to(Vector2(pos)) <= radius])
        return nearby_walls

    def get_merged_walls(self):
        merged_squares = []
        for i in range(len(self.tiles)):
            # if tile is already merged, iteration is skipped
            if self.tiles[i] in merged_squares:
                continue

            offset_x = self.grid_cell_size
            x_rect = [self.tiles[i]]

            offset_y = self.grid_cell_size
            y_rect = [self.tiles[i]]

            # adding nearby tiles (by x) to x_rect
            for j in range(len(self.tiles)):
                next_square_nearby = self.tiles[i].x + offset_x == self.tiles[j].x and self.tiles[i].y == self.tiles[j].y
                if next_square_nearby:
                    x_rect.append(self.tiles[j])
                    offset_x += self.grid_cell_size

            # adding nearby tiles (by y) to y_rect
            for l in range(len(self.tiles)):
                next_square_nearby = self.tiles[i].y + offset_y == self.tiles[l].y and self.tiles[i].x == self.tiles[l].x
                if next_square_nearby:
                    y_rect.append(self.tiles[l])
                    offset_y += self.grid_cell_size

            # merge bigger list of tiles to one rect and generate corresponding Wall
            if len(y_rect) > len(x_rect):
                merged_rect = Rect(y_rect[0].x, y_rect[0].y, self.grid_cell_size, len(y_rect) * self.grid_cell_size)
                self.walls.append(Wall(merged_rect, self))
                for square in y_rect:
                    merged_squares.append(square)
            else:
                merged_rect = Rect(x_rect[0].x, x_rect[0].y, len(x_rect) * self.grid_cell_size, self.grid_cell_size)
                self.walls.append(Wall(merged_rect, self))
                for square in x_rect:
                    merged_squares.append(square)


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
