import argparse
import numpy as np
import pygame as pg
from kalman import KalmanFilter

#----------------------------------------------------------------------------------------------------------
class Brick:

    STATE_X = 0
    STATE_Y = 1
    STATE_DX = 2
    STATE_DY = 3
    STATE_DDX = 4
    STATE_DDY = 5

    CONTROL_THRUST_X = 0
    CONTROL_THRUST_Y = 1

    COLOR = (0,0,255)

    def __init__(self, position, mass, thrust_power, noise_level):
        self.mass = mass
        self.thrust_power = thrust_power
        self.noise_level = noise_level
        self.state = [position[0], position[1], 0.0, 0.0, 0.0, 0.0]
        self.control = [0.0, 0.0]

    def tick(self, dt):
        A = self.__get_transition_matrix(dt)
        B = self.__get_control_matrix(dt)
        self.state = np.dot(A, self.state) + np.dot(B, self.control)
        w = np.multiply(self.state, self.__get_noise_vector())
        self.state += w

    def get_info_strings(self):
        zero = f'x = {self.state[self.STATE_X]:.3f}   y = {self.state[self.STATE_Y]:.3f}'
        first = f'dx = {self.state[self.STATE_DX]:.3f}   dy = {self.state[self.STATE_DY]:.3f}'
        second = f'ddx = {self.state[self.STATE_DDX]:.3f}   ddy = {self.state[self.STATE_DDY]:.3f}'
        control = f't_x = {self.control[self.CONTROL_THRUST_X]:.3f}   y = {self.control[self.CONTROL_THRUST_Y]:.3f}'
        return zero, first, second, control

    def __get_transition_matrix(self, dt):
        m = [
            [1.0, 0.0, dt, 0.0, dt*dt/2, 0.0], # x
            [0.0, 1.0, 0.0, dt, 0.0, dt*dt/2], # y
            [0.0, 0.0, 1.0, 0.0, dt, 0.0], # dx
            [0.0, 0.0, 0.0, 1.0, 0.0, dt], # dx
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # ddx
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # ddx
        ]
        return m

    def __get_control_matrix(self, dt):
        m=[
        [0.0, 0.0], # x
        [0.0, 0.0], # y
        [0.0, 0.0], # dx
        [0.0, 0.0], # dy
        [1/self.mass, 0.0], # ddx
        [0.0, 1/self.mass] # ddy
        ]
        return m

    def __get_noise_vector(self):
        noise = np.random.uniform(low=0.0-self.noise_level, high=self.noise_level, size=self.state.shape)
        noise[self.STATE_X] = 0.0
        noise[self.STATE_Y] = 0.0
        return noise

    def thrust_up(self):
        self.control[self.CONTROL_THRUST_Y] = 0-self.thrust_power/self.mass

    def thrust_down(self):
        self.control[self.CONTROL_THRUST_Y] = self.thrust_power/self.mass

    def thrust_left(self):
        self.control[self.CONTROL_THRUST_X] = 0-self.thrust_power/self.mass

    def thrust_right(self):
        self.control[self.CONTROL_THRUST_X] = self.thrust_power/self.mass

    def reset_thrust(self):
        self.control = [0.0, 0.0]


#----------------------------------------------------------------------------------------------------------
class Sensor:

    STATE_X = 0
    STATE_Y = 1
    STATE_DX = 2
    STATE_DY = 3
    STATE_DDX = 4
    STATE_DDY = 5

    COLOR = (255,0,0)

    HARD_NOISE_BASE = 1.0

    def __init__(self, position, noise_level, hard_noise, sensor_filter=None):
        self.state = [position[0], position[1], 0.0, 0.0, 0.0, 0.0]
        self.readouts = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.noise_level = noise_level
        self.hard_noise = hard_noise
        self.sensor_filter = sensor_filter

    def get_readout(self, brick_state, dt):
        readouts = np.dot(self.__get_measurement_matrix(dt), brick_state)
        v = np.multiply(readouts, self.__get_noise_vector())
        self.readouts = readouts + v

    def update_state(self):
        self.state = self.sensor_filter.process(self.state, self.readouts)
        
    def get_info_strings(self):
        zero = f'x = {self.state[self.STATE_X]:.3f}   y = {self.state[self.STATE_Y]:.3f}'
        first = f'dx = {self.state[self.STATE_DX]:.3f}   dy = {self.state[self.STATE_DY]:.3f}'
        return zero, first

    def __get_measurement_matrix(self, dt):
        m=[
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # x
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # y
            [0.0, 0.0, dt, 0.001*dt, -0.1*dt, 0.0], # dx
            [0.0, 0.0, 0.001*dt, dt, 0.0, -0.1*dt], # dx
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # ddx
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # ddx
        ]
        return m

    def __get_noise_vector(self):
        noise = np.random.uniform(low=0.0-self.noise_level, high=self.noise_level, size=len(self.state))
        noise[self.STATE_X] = 0.0
        noise[self.STATE_Y] = 0.0
        if np.random.uniform(1.0) < self.hard_noise:
            noise[self.STATE_DX] += np.random.uniform(0.0-self.HARD_NOISE_BASE, self.HARD_NOISE_BASE) 
        return noise


        
#----------------------------------------------------------------------------------------------------------
class GameEngine:

    FONT_SIZE = 30
    INITIAL_POSITION = (50,50)
    AGENT_SIZE = 20
    SENSOR_SIZE = 10
    BG_COLOR = (0,0,0)
    STATE_INFO_COLOR = (255,0,0)
    SENSOR_INFO_COLOR = (0,255,0)
    SCORE_INFO_COLOR = (255,255,0)


    def __init__(self,screen_width, screen_height, max_fps,
                 brick_mass, thruster_power, model_noise,
                 sensor_noise, hard_noise):
        self.running = True
        self.paused = False
        self.show_state_info = False
        self.show_sensor_info = False
        self.show_score = False
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.clock = pg.time.Clock()
        self.max_fps = max_fps
        self.font = pg.font.SysFont('Comic Sans MS', self.FONT_SIZE)
        self.agent = Brick(self.INITIAL_POSITION, brick_mass, thruster_power, model_noise)
        self.sensor = Sensor(self.INITIAL_POSITION, sensor_noise, hard_noise, KalmanFilter())
        self.text_cursor = [0,0]
        self.dt = 0
        self.cum_abs_error = 0.0
        self.dist = 0.0


    def main_loop(self):
        while self.running:
            self.tick()
        print(f'Cummulative absolute error = {self.cum_abs_error:.3f}')
        print(f'Distance travelled = {self.dist:.3f}')
        print(f'Final score = {self.get_score():.3f}')
        
    def tick(self):
        dt_millis = self.clock.tick(self.max_fps)
        self.dt = dt_millis / 1000.0
        self.agent.reset_thrust()
        self.handle_events()
        if not self.paused:
            self.agent.tick(self.dt)
            self.sensor.get_readout(self.agent.state, self.dt)
            self.sensor.update_state()
            self.update_score(self.dt)
        self.update_display()

    def get_score(self):
        return self.cum_abs_error/(self.dist+1.0)

    def update_score(self, dt):
        # dx in sensor is a readout and so it is already multiplied by dt
        dx = self.agent.state[Brick.STATE_DX]*dt
        dy = self.agent.state[Brick.STATE_DY]*dt
        sdx = self.sensor.state[Brick.STATE_DX]
        sdy = self.sensor.state[Brick.STATE_DX]
        self.dist += dx + dy
        self.cum_abs_error += abs(dx-sdx) + abs(dy-sdy)
        
    def get_rect_for_agent(self):
        return pg.Rect(self.agent.state[self.agent.STATE_X]-self.AGENT_SIZE/2,
                       self.agent.state[self.agent.STATE_Y]-self.AGENT_SIZE/2,
                       self.AGENT_SIZE, self.AGENT_SIZE)

    def get_rect_for_sensor(self):
        return pg.Rect(self.sensor.state[self.sensor.STATE_X]-self.SENSOR_SIZE/2,
                       self.sensor.state[self.sensor.STATE_Y]-self.SENSOR_SIZE/2,
                       self.SENSOR_SIZE, self.SENSOR_SIZE)

    def print_info(self):
        info_strs = self.agent.get_info_strings()
        for info in info_strs:
            text = self.font.render(info, False, self.STATE_INFO_COLOR)
            self.screen.blit(text, self.text_cursor)
            self.text_cursor[1] += self.FONT_SIZE

    def print_sensor(self):
        info_strs = self.sensor.get_info_strings()
        for info in info_strs:
            text = self.font.render(info, False, self.SENSOR_INFO_COLOR)
            self.screen.blit(text, self.text_cursor)
            self.text_cursor[1] += self.FONT_SIZE

    def print_score(self):        
        info_strings = [f'Travelled distance = {self.dist:.3f}']
        info_strings.append(f'Cumulative absolute error = {self.cum_abs_error:.3f}')
        info_strings.append(f'Score = {self.get_score():.3f}')
        for info in info_strings:
            text = self.font.render(info, False, self.SCORE_INFO_COLOR)
            self.screen.blit(text, self.text_cursor)
            self.text_cursor[1] += self.FONT_SIZE


        
    def update_display(self):
        self.screen.fill(self.BG_COLOR)
        self.text_cursor = [0,0]
        pg.draw.rect(self.screen, self.agent.COLOR, self.get_rect_for_agent())
        pg.draw.rect(self.screen, self.sensor.COLOR, self.get_rect_for_sensor())
        if self.show_state_info : self.print_info()
        if self.show_sensor_info : self.print_sensor()
        if self.show_score : self.print_score()
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == ord('q'):
                    self.running = False
                if event.key == ord('i'):
                    self.show_state_info = not self.show_state_info
                if event.key == ord('s'):
                    self.show_sensor_info = not self.show_sensor_info
                if event.key == ord('p'):
                    self.paused = not self.paused
                if event.key == ord('g'):
                    self.show_score = not self.show_score

        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.agent.thrust_up()
        if keys[pg.K_DOWN]:
            self.agent.thrust_down()
        if keys[pg.K_LEFT]:
            self.agent.thrust_left()
        if keys[pg.K_RIGHT]:
            self.agent.thrust_right()

#----------------------------------------------------------------------------------------------------------
def main(screen_width, screen_height, max_fps, brick_mass, thruster_power, model_noise, sensor_noise, hard_noise):
    pg.init()
    pg.font.init()
    game = GameEngine(screen_width, screen_height, max_fps, brick_mass,
                      thruster_power, model_noise, sensor_noise, hard_noise)
    game.main_loop()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--screen_width', type=int, default=400)
    parser.add_argument('-l', '--screen_height', type=int, default=300)
    parser.add_argument('-f', '--max_fps', type=int, default=60)
    parser.add_argument('-m', '--brick_mass', type=float, default=10.0)
    parser.add_argument('-t', '--thruster_power', type=float, default=10.0)
    parser.add_argument('-n', '--model_noise', type=float, default=0.0)
    parser.add_argument('-s', '--sensor_noise', type=float, default=0.0)
    parser.add_argument('-p', '--hard_noise', type=float, default=0.0)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args.screen_width, args.screen_height, args.max_fps,
         args.brick_mass, args.thruster_power, args.model_noise,
         args.sensor_noise, args.hard_noise)
