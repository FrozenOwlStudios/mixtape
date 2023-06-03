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

    def __init__(self, shape, initial_state=None):
        self.agregation = AggregationFunction()
        self.activation = ActivationFunction()
        self.update = UpdateFunction()
        self.grid = np.zeros(shape)
        if initial_state == 'GLIDER':
            self.grid = np.zeros((width, height))
            self.grid[50:55, 50:55] = NeuroConway.GLIDER

    def get_grid_height(self):
        return self.grid.shape[1]

    def get_grid_width(self):
        return self.grid.shape[0]

    def step(self, dt):
        if dt==0:
            return
        agreagation_grid = self.agregation(self.grid)
        activation_grid = self.activation(agreagation_grid, dt)
        self.grid = self.update(self.grid, activation_grid)


#==================================================================================================
#                                   PYGAME INTERFACE 
#==================================================================================================

class Display:
    
    BACKGROUND_BRIGHTNESS = 50
    MAX_BRIGHTNESS = 255
    BRIGHTNESS_RANGE = MAX_BRIGHTNESS-BACKGROUND_BRIGHTNESS

    def __init__(self, window_size, grid_size):
        self.window_size = window_size
        self.cell_size = (window_size[0]//grid_size[0], window_size[1]//grid_size[1])
        self.screen = None

    def init(self):
        self.screen = pg.display.set_mode(self.window_size)

    def draw_grid_cell(self, cell_grid):
        for x in range(cell_grid.get_grid_width()):
            for y in range(cell_grid.get_grid_height()):
                cell_brightness = BACKGROUND_BRIGHTNESS+cell_grid.grid[x][y]*BRIGHTNESS_RANGE
                cell_brightness = (cell_brightness, cell_brightness, cell_brightness)
                try:
                    pg.draw.rect(self.screen,
                                 cell_brightness,
                                (x*self.cell_size[0], y*self.cell_size[1], self.cell_size[0], self.cell_size[1]))
                except ValueError:
                    print(f'Problematic color {cell_brightness}')

    def flip(self):
        pg.display.flip() 


class SimulationState:

    MILLISECOND_TO_SECOND_RATIO = 1000

    def __init__(self):
        self.running = False
        self.paused = False
        self.clock = pg.time.Clock()
    
    def init(self):
        self.clock.tick()

    def tick(self):
        if not self.paused:
            return self.clock.tick()/SimulationState.MILLISECOND_TO_SECOND_RATIO
        return 0

    def toggle_pause(self):
        if self.paused:
            self.clock.tick()
        self.paused = not self.paused

class SimulationEngine:

    def __init__(self, game, display):
        self.game = game
        self.display = display
        self.state = SimulationState()

    def init(self):
        pg.init()
        self.display.init()
        self.state.init()
        
        #possible_neighborhood_values = np.linspace(0,8,100);
        #state_changes = NeuroConway.calculate_state_change(possible_neighborhood_values,1) 
        #plt.plot(possible_neighborhood_values, state_changes)
        #plt.show()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == ord('q'):
                    self.running = False
                elif event.key == ord('p'):
                    self.state.toggle_pause()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_presses = pg.mouse.get_pressed()
                if mouse_presses[0]:
                    x, y = pg.mouse.get_pos()
                    x = x//self.display.cell_size[0]
                    y = y//self.display.cell_size[1]
                    self.game.grid[x][y] = 1 - self.game.grid[x][y] 

    def run(self):
        self.running = True
        while self.running:
            self.display.draw_grid_cell(self.game)
            self.display.flip()
            self.handle_events()
            dt = self.state.tick()
            self.game.step(dt)



def main():
    grid_shape = (100, 100)
    window_shape = (800, 800)
    conway = NeuroConway(grid_shape,None)
    display = Display(window_shape, grid_shape)
    game = SimulationEngine(conway, display)
    game.init()
    game.run()

if __name__ == '__main__':
    main()
