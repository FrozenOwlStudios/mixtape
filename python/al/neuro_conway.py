import pygame as pg
import numpy as np
import cv2
import matplotlib.pyplot as plt

BACKGROUND_BRIGHTNESS = 50
MAX_BRIGHTNESS = 255
BRIGHTNESS_RANGE = MAX_BRIGHTNESS-BACKGROUND_BRIGHTNESS

#==================================================================================================
#                                   CELLULAR SYSTEM MECHANICS
#==================================================================================================

class AggregationFunction:

    CONWAY_KERNEL = np.array([
        [1.0, 1.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0]
        ])

    def __init__(self, kernel=None):
        self.kernel = kernel if kernel is not None else AggregationFunction.CONWAY_KERNEL
    
    def __call__(self, cell_grid):
        return cv2.filter2D(src=cell_grid, ddepth=-1, kernel=self.kernel)

class ActivationFunction:

    def __init__(self, median=2, div_squared=4, power=2, scale=2, shift=-1):
        self.median = median
        self.div_squared = div_squared
        self.power = power
        self.scale = scale
        self.shift = shift

    def __call__(self, agreagation_grid, dt):
        exponent = -np.power(agreagation_grid - self.median, self.power) / self.div_squared
        state_change = self.scale * np.exp(exponent) + self.shift
        return state_change * dt
        
class UpdateFunction:

    def __init__(self):
        pass

    def __call__(self, cell_grid, activation_grid):
        new_cell_grid = cell_grid + activation_grid
        return np.maximum(np.minimum(new_cell_grid,1),0)

class NeuroConway:


    GLIDER = np.array([
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0],
        [1.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 1.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
        ])

    def __init__(self, width, height, initial_state=None):
        self.agregation = AggregationFunction()
        self.activation = ActivationFunction()
        self.update = UpdateFunction()
        self.grid = np.zeros((width, height))
        if initial_state == 'GLIDER':
            self.grid = np.zeros((width, height))
            self.grid[50:55, 50:55] = NeuroConway.GLIDER

    def get_grid_height(self):
        return self.grid.shape[1]

    def get_grid_width(self):
        return self.grid.shape[0]


    def step(self, dt):
        agreagation_grid = self.agregation(self.grid)
        activation_grid = self.activation(agreagation_grid, dt)
        self.grid = self.update(self.grid, activation_grid)

class NcGame:

    def __init__(self, game, window_height, window_width):
        self.game = game
        self.window_width = window_width
        self.window_height = window_height
        self.cell_width = window_width//self.game.get_grid_width()
        self.cell_height = window_height//self.game.get_grid_height()
        self.running = False
        self.clock = pg.time.Clock()
        self.paused = False

    def initialze_pygame(self):
        pg.init()
        self.screen = pg.display.set_mode((self.window_width, self.window_height))
        
        #possible_neighborhood_values = np.linspace(0,8,100);
        #state_changes = NeuroConway.calculate_state_change(possible_neighborhood_values,1) 
        #plt.plot(possible_neighborhood_values, state_changes)
        #plt.show()


    def update(self):
        dt = self.clock.tick()/1000
        self.game.step(dt)

    def draw(self):
        for x in range(self.game.get_grid_width()):
            for y in range(self.game.get_grid_height()):
                cell_brightness = BACKGROUND_BRIGHTNESS+self.game.grid[x][y]*BRIGHTNESS_RANGE
                cell_brightness = (cell_brightness, cell_brightness, cell_brightness)
                try:
                    pg.draw.rect(self.screen,
                                 cell_brightness,
                                (x*self.cell_width, y*self.cell_height, self.cell_width, self.cell_height))
                except ValueError:
                    print(f'Problematic color {cell_brightness}')
        pg.display.flip() 
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == ord('q'):
                    self.running = False
                elif event.key == ord('p'):
                    self.paused = not self.paused
                    self.clock.tick() # To avoid time skips on unpausing
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_presses = pg.mouse.get_pressed()
                if mouse_presses[0]:
                    x, y = pg.mouse.get_pos()
                    x = x//self.cell_width
                    y = y//self.cell_height
                    self.game.grid[x][y] = 1 - self.game.grid[x][y] 

    def run(self):
        self.running = True
        while self.running:
            self.draw()
            self.handle_events()
            if not self.paused:
                self.update()



def main():
    conway = NeuroConway(100,100,None)
    game = NcGame(conway, 800,800)
    game.initialze_pygame()
    game.run()

if __name__ == '__main__':
    main()
