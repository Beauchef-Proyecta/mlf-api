import asyncio
from aiortc import (
    RTCPeerConnection,
    RTCConfiguration
)
import logging
from .videoShow import VideoShow, VideoBuffer
from .signaling import SignalingServer
from aiortc.contrib.media import MediaStreamTrack
from aiortc.contrib.signaling import BYE, add_signaling_arguments, create_signaling
from av import VideoFrame
import threading



class WebRTCUser():
    def __init__(self,address) -> None:
        # create signaling and peer connection
        self.signaling = SignalingServer(address)
        
        self.videoBuffer = VideoBuffer()

    def webRTCRecv(self):
        # run event loop
        self.pc = RTCPeerConnection(configuration=RTCConfiguration(iceServers=[]))
        self.__running = True
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.run())

        print("Stop webRTC")
        self.videoBuffer.stop()
        self.loop.run_until_complete(self.pc.close())
        

    def start(self):
        self.recvThread = threading.Thread(target=self.webRTCRecv, args=())
        self.recvThread.start()

    def close(self):
        self.__running = False
        self.recvThread.join()
        
        
    
    async def run(self):

        @self.pc.on("track")
        async def on_track(track):
            print("Receiving %s" % track.kind)
            if track.kind == 'video':
                await self.videoBuffer.addTrack(SimpleVideoTrack(track))
                if (not self.videoBuffer.started):
                    await self.videoBuffer.start()

            
        # send offer
        self.pc.addTransceiver('video', direction = 'recvonly')
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        response = await self.signaling.postOffer(self.pc.localDescription)
        await self.pc.setRemoteDescription(response)
        print("WebRTC ready")
        while self.__running:
            await asyncio.sleep(1)


class SimpleVideoTrack(MediaStreamTrack):

    kind = "video"

    def __init__(self, track):
        super().__init__()  # don't forget this!
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        return frame




if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    user = WebRTCUser("rainbowdash.local")
    user.start()