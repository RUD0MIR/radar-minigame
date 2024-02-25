import pygame
from pygame.sprite import Group


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.surface.get_size()[0] // 2
        self.half_h = self.surface.get_size()[1] // 2

        # ground
        # self.ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
        # self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))
        self.kpk = pygame.image.load(f"res/kpk.png").convert_alpha()

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player, walls: Group, rays: Group):
        self.center_target_camera(player)
        # active elements
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.surface.blit(sprite.image, offset_pos)

        for wall in walls.sprites():
            offset_pos = wall.rect.topleft - self.offset
            self.surface.blit(wall.image, offset_pos)

        for ray in rays.sprites():
            offset_pos = ray.rect.topleft - self.offset
            self.surface.blit(ray.image, offset_pos)

        self.surface.blit(self.kpk, (0, 0))