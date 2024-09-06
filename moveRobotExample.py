from mlf_api import RobotClient
import time

robot = RobotClient("fluttershy")

robot.set_joints(q0=0)
time.sleep(1)
robot.set_joints(q0=180)
time.sleep(1)
robot.set_joints(q0=0)
time.sleep(1)
robot.set_joints(q0=180)
