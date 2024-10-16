import requests
import json
import numpy as np
import cv2
from .webRTC import WebRTCController
from .videoShow import VideoShow

from .inverse_kinematics import inverse_kinematics


class RobotClient:

    robot_static_ips = {'applejack': "101", 'twilight': "102", "pinkiepie": "103", "fluttershy": "104", "rainbowdash": "105", "spike" : "106", "celestia": "107", "spirit": "108"}
    
    HOME_Q0 = 90
    HOME_Q1 = 90
    HOME_Q2 = 90

    def __init__(self, address, port=5000, portVideo=8080):
        self.address = address
        if self.address in self.robot_static_ips:
            self.address = "10.200.144." + self.robot_static_ips[self.address]
        print(self.address)
        self.port = port
        self.base_url = f"http://{self.address}:{port}"
        self.connected = False
        self.session = requests.Session()
        self.webRTCUser = WebRTCController(self.address)
    def connect(self):
        if self.connected:
            print("already connected :)")
            return

        url = f"{self.base_url}/connect"
        response = self.session.get(url)
        if response.status_code == 200:
            self.connected = True
            print(response.text)

    def move_xyz(self, x, y, z, eff_off = [56, 0, 0], q3=120):
        eff_off_x, eff_off_y, eff_off_z = eff_off
        q0, q1, q2 = inverse_kinematics(x, y, z, eff_off_x, eff_off_z)
        params = {"q0": q0, "q1": q1, "q2": q2, "q3": q3}
        url = f"{self.base_url}/set_joints"
        response = self.session.get(url, params=params)
        print(response.text)
        

    def set_joints(self, q0=90, q1=90, q2=90, q3=120):
        params = {"q0": q0, "q1": q1, "q2": q2, "q3": q3}
        url = f"{self.base_url}/set_joints"
        response = self.session.get(url, params=params)
        print(response.text)

    def set_relay_status(self, state=1, relay=1):
        params = {"state": state, "n_relay": relay}
        url = f"{self.base_url}/set_relay_status"
        response = self.session.get(url, params=params)
        print(response.text)
    
    def connectWebRTC(self):
        self.webRTCUser.connect()

    def set_extra_servo(self, q=0):
        params = {"q": q}
        url = f"{self.base_url}/set_extra_servo"
        response = self.session.get(url, params=params)
        print(response.text)

    def set_gripper_servo(self, q=120):
        params = {"q": q}
        url = f"{self.base_url}/set_gripper_servo"
        response = self.session.get(url, params=params)
        print(response.text)
    
    def get_weight(self):
        url = f"{self.base_url}/get_weight"
        response = self.session.get(url)
        json_data = json.loads(response.text)
        return json_data['weight']
    
    def get_distance(self):
        url = f"{self.base_url}/get_distance"
        response = self.session.get(url)
        json_data = json.loads(response.text)
        return json_data['distance']

    def closeWebRTC(self):
        self.webRTCUser.close()
        

    def showVideo(self, process= lambda frame : (frame, None)):
        self.webRTCUser.showVideo(process)
    
    def stopVideo(self):
        self.webRTCUser.stopVideo()
    

    def get_frame(self):
        return self.webRTCUser.getFrame()
    
    def capture(self):
        url = f"{self.base_url}/capture"
        response = self.session.get(url)
        # Convert the byte data to a numpy array
        image_data = np.frombuffer(response.content, np.uint8)
        
        # Decode the image from the numpy array
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        return image
        
    def home(self):
        self.set_joints(q0=self.HOME_Q0, q1=self.HOME_Q1, q2=self.HOME_Q2)