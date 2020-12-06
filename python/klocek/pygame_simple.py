import pygame as pg
import argparse
import numpy as np

class Robot:

    STATE_X = 0
    STATE_Y = 1
    STATE_DX = 2
    STATE_DY = 3
    STATE_DDX = 4
    STATE_DDY = 5
    STATE_THRUST_X = 6
    STATE_THRUST_Y = 7


    def __init__(self, x=0, y=0, width=60, height=60, mass=10, power=10):
        self.state_vector = np.asarray([x, y, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.measurement_vector = np.copy(self.state_vector) 
        self.width = width
        self.height = height
        self.mass = mass
        self.power = power

    def get_info_strings(self):
        zero = f'x = {self.state_vector[self.STATE_X]:.3f}   y = {self.state_vector[self.STATE_Y]:.3f}'
        first = f'dx = {self.state_vector[self.STATE_DX]:.3f}   dy = {self.state_vector[self.STATE_DY]:.3f}'
        second = f'ddx = {self.state_vector[self.STATE_DDX]:.3f}   ddy = {self.state_vector[self.STATE_DDY]:.3f}'
        thrust = f't_x = {self.state_vector[self.STATE_THRUST_X]:.3f}   y = {self.state_vector[self.STATE_THRUST_Y]:.3f}'
        return zero, first, second, thrust

    def create_measurement_matrix(self):
        # We only measure position
        m = [
            [1.0, 0.00001, -0.0001, 0.0, 0.0, 0.0, 0.0, 0.0], # x
            [0.00001, 1.0, 0.0, -0.0001, 0.0, 0.0, 0.0, 0.0], # y
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # dx
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # dx
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # ddx (THRUST IS MODELLED WIERDLY DO NOT WORRY ABOUT THAT)
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # ddx (THRUST IS MODELLED WIERDLY DO NOT WORRY ABOUT THAT)
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        return m


    def create_transition_matrix(self, dt):
        m = [
            [1.0, 0.0, dt, 0.0, dt*dt/2, 0.0, 0.0, 0.0], # x
            [0.0, 1.0, 0.0, dt, 0.0, dt*dt/2, 0.0, 0.0], # y
            [0.0, 0.0, 1.0, 0.0, dt, 0.0, 0.0, 0.0], # dx
            [0.0, 0.0, 0.0, 1.0, 0.0, dt, 0.0, 0.0], # dx
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0], # ddx (THRUST IS MODELLED WIERDLY DO NOT WORRY ABOUT THAT)
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], # ddx (THRUST IS MODELLED WIERDLY DO NOT WORRY ABOUT THAT)
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        return m

    def update(self, dt):
        self.state_vector = np.dot(self.create_transition_matrix(dt), self.state_vector)
        self.measurement_vector = np.dot(self.create_measurement_matrix(), self.state_vector)

    def get_rect(self):
        return self.state_vector[self.STATE_X], self.state_vector[self.STATE_Y], self.width, self.height

    def get_sensor_rect(self):
        return self.measurement_vector[self.STATE_X], self.measurement_vector[self.STATE_Y], self.width, self.height

    def thrust_up(self):
        self.state_vector[self.STATE_THRUST_Y] = 0-self.power/self.mass

    def thrust_down(self):
        self.state_vector[self.STATE_THRUST_Y] = self.power/self.mass

    def thrust_left(self):
        self.state_vector[self.STATE_THRUST_X] = 0-self.power/self.mass

    def thrust_right(self):
        self.state_vector[self.STATE_THRUST_X] = self.power/self.mass


    

class Game:

    def __init__(self):
        self.running = False
        self.screen = None
        self.clock = None
        self.max_fps = 0
        self.robot = Robot(x=60, y=60)
        self.dt = 0.0
        self.font = None
        self.show_info = False
        self.text_cursor = [0,0]
        self.text_step = 20
        self.state_info_clr = (255,0,0)
        self.sensor_info_clr = (0,255,0)

    def initialize(self, screen_width, screen_height, max_fps):
        self.running = True
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.clock = pg.time.Clock()
        self.max_fps = max_fps
        self.font = pg.font.SysFont('Comic Sans MS', 30)

    def tick(self):
        dt_millis = self.clock.tick(self.max_fps)
        self.dt = dt_millis / 1000.0
        self.handle_events()
        self.robot.update(self.dt)
        self.update_display()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == ord('q'):
                    self.running = False
                if event.key == ord('i'):
                    self.show_info = not self.show_info
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.robot.thrust_up()
        if keys[pg.K_DOWN]:
            self.robot.thrust_down()
        if keys[pg.K_LEFT]:
            self.robot.thrust_left()
        if keys[pg.K_RIGHT]:
            self.robot.thrust_right()

    def print_info(self):
        info_strs = self.robot.get_info_strings()
        step = 20
        self.text_cursor = [0,0]
        for info in info_strs:
            text = self.font.render(info, False, self.state_info_clr)
            self.screen.blit(text, self.text_cursor)
            self.text_cursor[1] += self.text_step
            
    def update_display(self):
        self.screen.fill((0,0,0))
        pg.draw.rect(self.screen, (128, 0, 128), pg.Rect(self.robot.get_sensor_rect()))
        pg.draw.rect(self.screen, (0, 128, 255), pg.Rect(self.robot.get_rect()))
        if self.show_info : self.print_info()
        pg.display.flip()

    def __bool__(self):
        return self.running


def main(screen_width, screen_height, max_fps):
    game = Game()
    pg.init()
    pg.font.init()
    game.initialize(screen_width, screen_height, max_fps)
    while game:
        game.tick()
        
    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--screen_width', type=int, default=400)
    parser.add_argument('-l', '--screen_height', type=int, default=300)
    parser.add_argument('-f', '--max_fps', type=int, default=60)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args.screen_width, args.screen_height, args.max_fps)
