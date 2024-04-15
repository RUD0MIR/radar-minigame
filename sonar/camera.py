import pygame
from pygame import Rect
from pygame.sprite import Group


class CameraGroup(pygame.sprite.Group):
    """
    draws all objects with offset that depends on target's position
    """
    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.surface.get_size()[0] // 2
        self.half_h = self.surface.get_size()[1] // 2

        self.kpk = pygame.image.load(f"res/img/kpk.png").convert_alpha()

    def center_camera(self, target: Rect):
        self.offset.x = target.centerx - self.half_w
        self.offset.y = target.centery - self.half_h

    def custom_draw(self, target: Rect, groups: list[Group]):
        self.center_camera(target)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.surface.blit(sprite.image, offset_pos)
        for group in groups:
            for sprite in group.sprites():
                offset_pos = sprite.rect.topleft - self.offset
                self.surface.blit(sprite.image, offset_pos)

        self.surface.blit(self.kpk, (0, 0))
