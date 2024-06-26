from mlf_api import RobotClient
import time

robot = RobotClient("rainbowdash.local")

robot.set_joints(q0=-40)
robot.set_joints(q0=40)
robot.set_joints(q0=-40)
robot.set_joints(q0=40)
