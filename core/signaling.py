import aiohttp
from aiortc import RTCSessionDescription
import json
import asyncio

class SignalingServer():
    def __init__(self, address, port= 8080) -> None:
        self.url = f'http://{address}:{port}/offer' #Url de host
    
    async def postOffer(self, localDescription) -> RTCSessionDescription:
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}, trust_env=True) as session:
            print("Connected")
            params =  {"sdp": localDescription.sdp, "type": localDescription.type}
            async with session.post(self.url, json= params) as response:
                text = await response.text()
                message = json.loads(text)
                return RTCSessionDescription(**message)