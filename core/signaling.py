import aiohttp
from aiortc import RTCSessionDescription
import json
from mlfApi import PORT, IP

class SignalingServer():
    def __init__(self) -> None:
        self.url = f'http://{IP}:{PORT}/offer' #Url de hos
    
    async def postOffer(self, localDescription) -> RTCSessionDescription:
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}, trust_env=True) as session:
            print("Connected")
            params =  {"sdp": localDescription.sdp, "type": localDescription.type}
            async with session.post(self.url, json= params) as response:
                text = await response.text()
                message = json.loads(text)
                return RTCSessionDescription(**message)