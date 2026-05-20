import pygame as pg
import sys

# Initialize pg
pg.init()

# Const
WIDTH = 500
HEIGHT = 500
GRID_PRECISION_MIN = 10
GRID_PRECISION_MAX = 50
GRID_PRECISION_STEP = 10


# Create a 500x500 window
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Owl")

# Colors
BACKGROUND = (0, 0, 0)
BODY = (139, 69, 19)
GRID = (255, 0, 0)

# State
running = True
draw_grid = False
grid_precision = GRID_PRECISION_MIN

# Main loop

while running:
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == ord('g'):
                draw_grid = not draw_grid
            elif event.key == ord('q'):
                running = False
            elif event.key == ord('p'):
                grid_precision += GRID_PRECISION_STEP
                if grid_precision > GRID_PRECISION_MAX:
                    grid_precision = GRID_PRECISION_MIN

    # Fill background with black
    screen.fill(BACKGROUND)

    # Draw a brown rectangle
    pg.draw.rect(screen, BODY, (150, 200, 200, 100))
    # Format: (x, y, width, height)


    # If draw grid set to true draw it on top of everything else
    if draw_grid:
        for x in range(0, WIDTH, grid_precision):
            pg.draw.line(screen, GRID, (x,0), (x,HEIGHT))
        for y in range(0, HEIGHT, grid_precision):
            pg.draw.line(screen, GRID, (0,y), (WIDTH,y))

    # Update display
    pg.display.flip()

# Quit pg
pg.quit()
sys.exit()