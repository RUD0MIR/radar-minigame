import pygame

pygame.init()
font = pygame.font.Font(None, 30)


def logd(info, y=0, x=0):
    surface = pygame.display.get_surface()
    text = font.render(str(info), True, 'white')
    rect = text.get_rect(topleft=(x + 10, y + 10))
    pygame.draw.rect(surface, 'Black', rect)
    surface.blit(text, rect)
