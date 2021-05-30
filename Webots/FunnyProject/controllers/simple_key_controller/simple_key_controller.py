from controller import Robot
from controller import Keyboard

FORWARD_SPEED = 5.0
TURN_SPEED = FORWARD_SPEED/2.0

robot = Robot()
timestep = int(robot.getBasicTimeStep())
#timestep = 64 # In case if getBasicTimeStep() causes errors

wheel_left = robot.getDevice('left wheel')
wheel_right = robot.getDevice('right wheel')
wheel_left.setPosition(float('inf'))
wheel_right.setPosition(float('inf'))
wheel_left.setVelocity(0.0)
wheel_right.setVelocity(0.0)

camera = robot.getDevice('kinect color')
camera.enable(timestep)

keyboard = Keyboard()
keyboard.enable(timestep)

motor_commands = {
        ord('W'): (FORWARD_SPEED, FORWARD_SPEED),
        ord('S'): (-FORWARD_SPEED, -FORWARD_SPEED),
        ord('A'): (-TURN_SPEED, TURN_SPEED),
        ord('D'): (TURN_SPEED, -TURN_SPEED),
        ord('E'): (0.0, 0.0)
        }

while robot.step(timestep) != -1:
    key = keyboard.getKey()
    if key in motor_commands.keys():
        wheel_left.setVelocity(motor_commands[key][0])
        wheel_right.setVelocity(motor_commands[key][1])
