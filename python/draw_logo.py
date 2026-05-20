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
BACKGROUND = (120, 166, 206) # Of workbench
BODY_BACK = (78, 48, 25)
BODY_FRONT = (135, 89, 49)
HEAD = BODY_FRONT
EYE_BACK = (172, 95, 1)
EYE_FRONT = (0,0,0)
EYE_GLIMMER = (255,255,255)
BEAK = (79,71,61)
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
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            print(f"Mouse clicked at: ({mouse_x}, {mouse_y})")

    # Fill background with black
    screen.fill(BACKGROUND)


    # Main body
    pg.draw.circle(screen, BODY_BACK, (250,300), 150)

    # Head on top
    pg.draw.circle(screen, BODY_BACK, (250,220), 120)
    pg.draw.circle(screen, HEAD, (250,220), 95)

    # Ears (by cutting into head)
    pg.draw.arc(screen, BACKGROUND, pg.Rect((130, 100) , (240, 240)), 1, 2.14, width=25)

    # Front plumage
    pg.draw.polygon(screen, BODY_FRONT, [
        (155,222),
        (346,221),
        (295,442),
        (202,442)
        
    ])
    #pg.draw.arc(screen, GRID, pg.Rect((130, 100) , (240, 240)), 1, 2.14, width=25)

    # Beak
    pg.draw.polygon(screen, BEAK, [
        (220,200),
        (250,270),
        (280,200),
    ])

    
    # Eyes
    pg.draw.circle(screen, EYE_BACK, (200,200), 50)
    pg.draw.circle(screen, EYE_FRONT, (200,200), 40)
    pg.draw.circle(screen, EYE_GLIMMER, (180,180), 8)
    pg.draw.circle(screen, EYE_BACK, (300,200), 50)
    pg.draw.circle(screen, EYE_FRONT, (300,200), 40)
    pg.draw.circle(screen, EYE_GLIMMER, (280,180), 8)

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