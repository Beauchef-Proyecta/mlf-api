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



class WebRTCController():
    def __init__(self,address) -> None:
        # create signaling and peer connection
        self.signaling = SignalingServer(address)
        self.cond = threading.Condition()
        self.videoBuffer = VideoBuffer(self.cond)
        self.videoShow = VideoShow(self.videoBuffer)
        self.connected = False

    def webRTCRecv(self):
        # run event loop
        self.pc = RTCPeerConnection(configuration=RTCConfiguration(iceServers=[]))
        self.__running = True
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.run())

        print("Ending WebRTC connection")
        self.loop.run_until_complete(self.pc.close())
        

    def connect(self):
        with self.cond:
            self.recvThread = threading.Thread(target=self.webRTCRecv, args=())
            self.recvThread.start()
            self.cond.wait()
        self.connected = True
        print("WebRTC connection ready")

    def close(self):
        if self.videoShow.isRunning():
            self.stopVideo()
        self.__running = False
        self.recvThread.join()

    def getFrame(self):
        if not self.connected:
            self.connect()
        return self.videoBuffer.getCurrentFrame()

    def showVideo(self, process):
        if not self.connected:
            self.connect()
        if not self.videoShow.isRunning():
            self.videoShow.start(process)
        else:
            print("Already showing video")
    
    def stopVideo(self):
        self.videoShow.stop()
        
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
        while self.__running:
            await asyncio.sleep(1)
        await self.videoBuffer.stop()


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
    user = WebRTCController("rainbowdash.local")
    user.start()