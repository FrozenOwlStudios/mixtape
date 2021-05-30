from controller import Robot
from controller import Keyboard
import struct
import cv2
import numpy as np
import os


class PDcontroller:

    def __init__(self, p, d, sampling_period, target=0.0):
        self.target = target
        self.response = 0.0
        self.old_error = 0.0
        self.p = p
        self.d = d
        self.sampling_period = sampling_period

    def process_measurement(self, measurement):
        error = self.target - measurement
        derivative = (error - self.old_error)/self.sampling_period
        self.old_error = error
        self.response = self.p*error + self.d*derivative
        return self.response

    def reset(self):
        self.target = 0.0
        self.response = 0.0
        self.old_error = 0.0


class MotorController:

    def __init__(self, name, robot, pd):
        self.name = name
        self.robot = robot
        self.pd = pd
        self.motor = None
        self.velocity = 0.0

    def enable(self):
        self.motor = self.robot.getDevice(self.name)
        self.motor.setPosition(float('inf'))
        self.motor.setVelocity(0.0)

    def update(self):
        self.velocity += self.pd.process_measurement(self.motor.getVelocity())
        self.motor.setVelocity(self.velocity)

    def set_target(self, target):
        self.pd.target = target

    def emergency_stop(self):
        self.motor.setVelocity(0.0)
        self.pd.reset()
        self.velocity = 0.0


class MotorCommand:

    def __init__(self, left_velocity, right_velocity, emergency_stop=False):
        self.left_velocity = left_velocity
        self.right_velocity = right_velocity
        self.emergency_stop = emergency_stop

class Camera:

    __CHANNELS = 4

    def __init__(self, name, screenshot_folder=None):
        self.name = name
        self.frame = None
        self.image_byte_size = None
        self.device = None
        self.screenshot_folder = screenshot_folder
        self.screenshot_id = 0

    def enable(self, timestep):
        self.device = robot.getDevice(self.name)
        self.device.enable(timestep)
        self.image_byte_size = self.device.getWidth()*self.device.getHeight()*Camera.__CHANNELS
        if self.screenshot_folder is not None:
            for filename in os.listdir(self.screenshot_folder):
                if filename.endswith('.png'):
                    try:
                        screenshot_id = int(filename.split('.')[0])
                        if screenshot_id > self.screenshot_id:
                            self.screenshot_id = screenshot_id
                    except Exception:
                        # If exception happens then file is not named according to our 
                        # pattern and we do not worry about it.
                        pass
            self.screenshot_id += 1

    def get_frame(self):
        frame = self.device.getImage()
        if frame is None:
            return self.frame
        frame = struct.unpack(f'{self.image_byte_size}B', frame)
        frame = np.array(frame, dtype=np.uint8).reshape(self.device.getHeight(),
                self.device.getWidth(), Camera.__CHANNELS)
        frame = frame[:,:,0:3]
        self.frame = frame
        return frame

    def show_frame(self, scale=1.0):
        scaled_frame = cv2.resize(self.frame, (0,0), fx=scale, fy=scale)
        cv2.imshow(self.name, scaled_frame)

    def save_frame(self):
        cv2.imwrite(f'{self.screenshot_folder}/{self.screenshot_id}.png', self.frame)
        self.screenshot_id += 1


FORWARD_SPEED = 5.0
TURN_SPEED = FORWARD_SPEED/2.0

motor_commands = {
        ord('W'): MotorCommand(FORWARD_SPEED, FORWARD_SPEED),
        ord('X'): MotorCommand(-FORWARD_SPEED, -FORWARD_SPEED),
        ord('A'): MotorCommand(-TURN_SPEED, TURN_SPEED),
        ord('D'): MotorCommand(TURN_SPEED, -TURN_SPEED),
        ord('S'): MotorCommand(0.0, 0.0),
        ord('E'): MotorCommand(0.0, 0.0, True)
        }


robot = Robot()
timestep = 64 #int(robot.getBasicTimeStep())
timestep_seconds = timestep/1000.0

motor_left = MotorController('left wheel', robot, PDcontroller(0.01, 0.0001, timestep_seconds))
motor_right = MotorController('right wheel', robot, PDcontroller(0.01, 0.0001, timestep_seconds))
motor_left.enable()
motor_right.enable()

cv2.startWindowThread()
camera = Camera('kinect color', '../../screenshots')
camera.enable(timestep)


keyboard = Keyboard()
keyboard.enable(timestep)

PHOTO_PERIOD = 1
last_photo_timestamp = 0
timestamp = 0
auto_photo_mode = False

while robot.step(timestep) != -1:
    timestamp += timestep
    camera.get_frame()
    camera.show_frame(scale=3.0)
    motor_left.update()
    motor_right.update()
    key = keyboard.getKey()
#    print(f'Timestamp - {timestamp}')
    if auto_photo_mode and timestamp - last_photo_timestamp >= PHOTO_PERIOD*1000:
       camera.save_frame()
       last_photo_timestamp = timestamp
       print(f'Took photo at {timestamp//1000} second mark.')
    if key in motor_commands.keys():
        cmd = motor_commands[key]
        if cmd.emergency_stop:
            motor_left.emergency_stop()
            motor_right.emergency_stop()
        else:
            motor_left.set_target(cmd.left_velocity)
            motor_right.set_target(cmd.right_velocity)
    elif key == ord('Z'):
        print(os.system('pwd'))
    elif key == ord('Q'):
        camera.save_frame()
    elif key == ord('P'):
        auto_photo_mode = not auto_photo_mode
        print(f'Auto photo mode {"enable" if auto_photo_mode else "disabled"}')
    cv2.waitKey(timestep)
