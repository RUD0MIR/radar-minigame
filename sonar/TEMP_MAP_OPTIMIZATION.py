import pygame
from pygame.rect import Rect

import pygame


def merge_squares(squares: [Rect]):
    final_rects = []
    merged_squares = []
    for i in range(len(squares)):
        if squares[i] in merged_squares:
            continue

        next_offset = 20
        current_rect = [squares[i]]

        for j in range(len(squares)):
            next_square_nearby = squares[i].y + next_offset == squares[j].y and squares[i].x == squares[j].x
            if next_square_nearby:
                current_rect.append(squares[j])
                merged_squares.append(squares[j])
                next_offset += 20

        final_rects.append(Rect(current_rect[0].x, current_rect[0].y, 20, len(current_rect) * 20))
        current_rect.clear()
    return final_rects


# Example usage
pygame.init()
screen = pygame.display.set_mode((800, 600))

rectangles = [
    Rect(0, 0, 20, 20), Rect(0, 20, 20, 20), Rect(0, 40, 20, 20), Rect(20, 0, 20, 20),
    Rect(40, 0, 20, 20),
    Rect(60, 0, 20, 20),
    Rect(100, 100, 20, 20)
]
running = True

for rect in rectangles:
    surface = pygame.Surface((rect.width, rect.height))
    surface.fill('red')

    screen.blit(surface, rect)

xoffset = 20
for rect in merge_squares(rectangles):
    offset_rect = Rect(rect.x + 120 + xoffset, rect.y, rect.width, rect.height)

    surface1 = pygame.Surface((rect.width, rect.height))
    surface1.fill('green')

    screen.blit(surface1, offset_rect)
    xoffset += 20

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
