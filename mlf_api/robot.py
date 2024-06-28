import requests
import json
from .webRTC import WebRTCController
from .videoShow import VideoShow

from .inverse_kinematics import inverse_kinematics


class RobotClient:
    
    HOME_Q0 = 0
    HOME_Q1 = 0
    HOME_Q2 = 90

    def __init__(self, address, port=5000, portVideo=8080):
        self.address = address
        self.port = port
        self.base_url = f"http://{address}:{port}"
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
        

    def set_joints(self, q0=0, q1=0, q2=90, q3=120):
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
        return json_data['weight'][0]
    
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
        
    def home(self):
        self.set_joints(q0=self.HOME_Q0, q1=self.HOME_Q1, q2=self.HOME_Q2)