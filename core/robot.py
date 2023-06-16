import requests
from .user import WebRTCUser
from .videoShow import VideoShow


class RobotClient:
    
    HOME_Q0 = 0
    HOME_Q1 = 0
    HOME_Q2 = 90

    def __init__(self, address, port=5000, portVideo=8080):
        self.address = address
        self.port = port
        self.base_url = f"http://{address}:{port}"
        self.connected = False
        self.webRTCConnect = False

    def connect(self):
        if self.connected:
            print("already connected :)")
            return

        url = f"{self.base_url}/connect"
        response = requests.get(url)
        if response.status_code == 200:
            self.connected = True
            print(response.text)

    def move_xyz(self, x, y, z):
        params = {"x": x, "y": y, "z": z}
        url = f"{self.base_url}/move"
        response = requests.get(url, params=params)
        print(response.text)
        

    def set_joints(self, q0=0, q1=0, q2=90):
        params = {"q0": q0, "q1": q1, "q2": q2}
        url = f"{self.base_url}/set_joints"
        response = requests.get(url, params=params)
        print(response.text)
    
    def __connectWebRTC(self):
        self.webRTCUser = WebRTCUser(self.address)
        self.webRTCUser.start()
        self.webRTCConnect = True

    def closeWebRTC(self):
        self.webRTCUser.close()
        self.videoShow.stop()

    def showVideo(self):
        if not self.webRTCConnect:
            self.__connectWebRTC()
        self.videoShow = VideoShow(self.webRTCUser.videoBuffer)
        self.videoShow.start()
    

    def get_frame(self):
        if not self.webRTCConnect:
            self.__connectWebRTC()
        return self.webRTCUser.videoBuffer.getCurrentFrame()
        
    def home(self):
        self.set_joints(q0=self.HOME_Q0, q1=self.HOME_Q1, q2=self.HOME_Q2)