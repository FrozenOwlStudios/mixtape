import argparse
import pygame as pg
import numpy as np
import cv2
import matplotlib.pyplot as plt

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

    def __init__(self, shape, agregation, activation, update):
        self.agregation = agregation
        self.activation = activation 
        self.update = update 
        self.grid = np.zeros(shape)
        #if initial_state == 'GLIDER':
        #    self.grid = np.zeros((width, height))
        #    self.grid[50:55, 50:55] = NeuroConway.GLIDER

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
                cell_brightness = Display.BACKGROUND_BRIGHTNESS+cell_grid.grid[x][y]*Display.BRIGHTNESS_RANGE
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
        self.running = True
        self.clock.tick()

    def tick(self):
        if not self.paused:
            return self.clock.tick()/SimulationState.MILLISECOND_TO_SECOND_RATIO
        return 0

    def toggle_pause(self):
        if self.paused:
            self.clock.tick()
        self.paused = not self.paused


class KeyboardHandler:

    def __init__(self, simulation_state, simulation_engine):
        self.simulation_state = simulation_state
        self.simulation_engine = simulation_engine

    def handle_event(self, event):
        if event.key == ord('q'):
            self.simulation_state.running = False
        elif event.key == ord('p'):
            self.simulation_state.toggle_pause()
        elif event.key == ord('a'):
            self.simulation_engine.plot_activations()

class MouseHandler:

    def __init__(self, simulation_state, display, cell_grid):
        self.simulation_state = simulation_state
        self.display = display
        self.cell_grid = cell_grid

    def handle_event(self, event):
        mouse_presses = pg.mouse.get_pressed()
        if mouse_presses[0]:
            x, y = pg.mouse.get_pos()
            x = x//self.display.cell_size[0]
            y = y//self.display.cell_size[1]
            self.cell_grid.grid[x][y] = 1 - self.cell_grid.grid[x][y] 

class SimulationEngine:

    def __init__(self, cell_grid, display):
        self.cell_grid=cell_grid 
        self.display = display
        self.state = SimulationState()
        self.keyboard = KeyboardHandler(self.state, self)
        self.mouse = MouseHandler(self.state, self.display, self.cell_grid)

    def init(self):
        pg.init()
        self.display.init()
        self.state.init()
        
    def plot_activations(self):
        aggergation_vector = np.linspace(0,8,100);
        activation_vector = self.cell_grid.activation(aggergation_vector,1) 
        plt.plot(aggergation_vector, activation_vector)
        plt.show()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.state.running = False
            elif event.type == pg.KEYDOWN:
                self.keyboard.handle_event(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse.handle_event(event)

    def run(self):
        while self.state.running:
            self.display.draw_grid_cell(self.cell_grid)
            self.display.flip()
            self.handle_events()
            dt = self.state.tick()
            self.cell_grid.step(dt)


#==================================================================================================
#                                MAIN FUNCTION AND ARGUMENT PARSING 
#==================================================================================================

def size2D(txt):
    return tuple(map(int,txt.split('x')))

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--median', type=float, default=3.0,
                        help='Median of activation function')
    parser.add_argument('-d', '--divergence_squared', type=float, default=4.0,
                        help='Parameter that effects width of curve')
    parser.add_argument('-p', '--power', type=int, default=2,
                        help='Power used in activation function')
    parser.add_argument('-s', '--scale', type=float, default=2.0,
                        help='Scale used in activation function')
    parser.add_argument('-f', '--shift', type=float, default=-1.0,
                        help='Shift used in activation function')
    parser.add_argument('--grid_shape', type=size2D, default=(100, 100),
                        help='Size of cellular grid')
    parser.add_argument('--window_shape', type=size2D, default=(800, 800),
                        help='Size of program main window in pixels')
    return parser.parse_args()

#median=2, div_squared=4, power=2, scale=2, shift=-1):
def main(args):
    agregation = AggregationFunction()
    activation = ActivationFunction(args.median, args.divergence_squared, args.power,
                                    args.scale, args.shift)
    update = UpdateFunction()
    conway = NeuroConway(args.grid_shape, agregation, activation, update)
    display = Display(args.window_shape, args.grid_shape)
    game = SimulationEngine(conway, display)
    game.init()
    #game.plot_activations()
    game.run()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
