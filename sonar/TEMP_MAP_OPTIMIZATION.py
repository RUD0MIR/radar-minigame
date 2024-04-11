import pygame
from pygame.rect import Rect

import pygame


def merge_squares_x(squares: [Rect]):
    final_rects = []
    merged_squares = []
    for i in range(len(squares)):
        if squares[i] in merged_squares:
            continue

        next_offset = 20
        current_rect = [squares[i]]

        for j in range(len(squares)):
            next_square_nearby = squares[i].x + next_offset == squares[j].x and squares[i].y == squares[j].y
            if next_square_nearby:
                current_rect.append(squares[j])
                merged_squares.append(squares[j])
                next_offset += 20

        final_rects.append(Rect(current_rect[0].x, current_rect[0].y, len(current_rect) * 20, 20))
        current_rect.clear()
    return final_rects


def merge_squares(squares: [Rect], size: int):
    final_rects = []
    merged_squares = []
    for i in range(len(squares)):
        if squares[i] in merged_squares:
            continue

        offset_x = size
        x_rect = [squares[i]]

        offset_y = size
        y_rect = [squares[i]]

        for j in range(len(squares)):
            next_square_nearby = squares[i].x + offset_x == squares[j].x and squares[i].y == squares[j].y
            if next_square_nearby:
                x_rect.append(squares[j])
                offset_x += size

        for l in range(len(squares)):
            next_square_nearby = squares[i].y + offset_y == squares[l].y and squares[i].x == squares[l].x
            if next_square_nearby:
                y_rect.append(squares[l])
                offset_y += size

        if len(y_rect) > len(x_rect):
            final_rects.append(Rect(y_rect[0].x, y_rect[0].y, size, len(y_rect) * size))
            for square in y_rect:
                merged_squares.append(square)
        else:
            final_rects.append(Rect(x_rect[0].x, x_rect[0].y,  len(x_rect) * size, size))
            for square in x_rect:
                merged_squares.append(square)

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
print(len(rectangles))
print(len(merge_squares(rectangles, 20)))
offset = 20
for rect in merge_squares(rectangles, 20):
    # offset_rect = Rect(rect.x + 120 + offset, rect.y + offset, rect.width, rect.height)
    offset_rect = Rect(rect.x + 120, rect.y, rect.width, rect.height)

    surface1 = pygame.Surface((rect.width, rect.height))
    surface1.fill('green')

    screen.blit(surface1, offset_rect)
    offset += 20

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
