from core.robot import RobotClient
import time
import cv2
import numpy as np

def onlyColor(frame):
  # It converts the BGR color space of image to HSV color space
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      
  # Threshold of blue in HSV space
  lower_green = np.array([50,100,50])
  upper_green = np.array([90,255,255])

  # Threshold the HSV image to get only blue colors
  mask = cv2.inRange(hsv, lower_green, upper_green)

  # Bitwise-AND mask and original image
  output = cv2.bitwise_and(frame,frame, mask= mask)
  return output, None


robot = RobotClient("rainbowdash.local")

robot.showVideo(process= onlyColor)

time.sleep(10)

robot.closeWebRTC()
