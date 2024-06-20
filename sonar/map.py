import pygame
from pygame import Rect, Vector2
from pygame.sprite import Group, Sprite

from sonar import const
from sonar.const import black


class Wall(pygame.sprite.Sprite):
    """
    simple rectangular Sprite, player can collide with
    """
    def __init__(self, rect: Rect, group: Group):
        super().__init__(group)
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image.fill('white')
        # self.image.fill(black)

        self.alpha = 0
        self.alpha_decrease_rate = 0.5
        self.alpha_counter = -1
        self.alpha_counter_max_value = 150
        self.image.set_alpha(self.alpha)


class Walls(pygame.sprite.Group):
    """
        group of Wall sprites generated from tmx files
    """
    def __init__(self, surface, tmx_layers, cell_size):
        super().__init__()
        self.surface = surface
        self.walls = []
        self.grid_cell_size = cell_size
        self.tmx_layers = tmx_layers
        self.tiles = []
        self.filled_tiles = []

        self.get_tiles_from_tmx()
        self.get_merged_walls(self.tiles, False)
        self.get_merged_walls(self.filled_tiles, True)

    def get_tiles_from_tmx(self):
        """
        converts tiles from tmx file on a layer 'walls' to Wall sprites using pytmx
        """
        for layer in self.tmx_layers:
            if layer.name == 'walls':
                for x, y, surf in layer.tiles():
                    pos = (x * self.grid_cell_size, y * self.grid_cell_size)
                    rect = pygame.Rect(pos, (self.grid_cell_size, self.grid_cell_size))
                    self.tiles.append(rect)

    def get_nearby_walls(self, pos, radius):
        """
        returns list of walls within certain radius from pos
        """
        nearby_walls = Group()
        nearby_walls.add([wall for wall in self.walls if Vector2(wall.rect.center).distance_to(Vector2(pos)) <= radius])
        return nearby_walls

    def get_merged_walls(self, tiles, is_filled):
        """
        merging nearby tiles to bigger ones, making less sprites overall
        """
        merged_squares = []
        for i in range(len(tiles)):
            # if tile is already merged, iteration is skipped
            if tiles[i] in merged_squares:
                continue

            offset_x = self.grid_cell_size
            x_rect = [tiles[i]]

            offset_y = self.grid_cell_size
            y_rect = [tiles[i]]

            # adding nearby tiles (by x) to x_rect
            for j in range(len(tiles)):
                next_square_nearby = tiles[i].x + offset_x == tiles[j].x and tiles[i].y == tiles[j].y
                if next_square_nearby:
                    x_rect.append(tiles[j])
                    offset_x += self.grid_cell_size

            # adding nearby tiles (by y) to y_rect
            for l in range(len(tiles)):
                next_square_nearby = tiles[i].y + offset_y == tiles[l].y and tiles[i].x == tiles[l].x
                if next_square_nearby:
                    y_rect.append(tiles[l])
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
