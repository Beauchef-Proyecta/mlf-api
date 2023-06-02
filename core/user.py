import asyncio
from aiortc import (
    RTCPeerConnection,
    RTCConfiguration
)
import logging
from videoShow import VideoShow, VideoBuffer
from signaling import SignalingServer
from aiortc.contrib.media import MediaStreamTrack
from aiortc.contrib.signaling import BYE, add_signaling_arguments, create_signaling
from av import VideoFrame



class WebRTCuser():
    def __init__(self) -> None:
        # create signaling and peer connection
        self.signaling = SignalingServer()
        self.pc = RTCPeerConnection(configuration=RTCConfiguration(iceServers=[]))
        self.videoBuffer = VideoBuffer()

    def start(self):
        # run event loop
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                self.run()
            )
        except KeyboardInterrupt:
            pass
        finally:
            # cleanup
            self.videoBuffer.stop()
            loop.run_until_complete(self.pc.close())
    
    async def run(self):

        @self.pc.on("track")
        async def on_track(track):
            print("Receiving %s" % track.kind)
            if track.kind == 'video':
                await self.videoBuffer.addTrack(SimpleVideoTrack(track))
                if (not self.videoBuffer.started):
                    print("initialized")
                    await self.videoBuffer.start(showVideo=True)
                    print("initialized")

            
        # send offer
        self.pc.addTransceiver('video', direction = 'recvonly')
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        response = await self.signaling.postOffer(self.pc.localDescription)
        await self.pc.setRemoteDescription(response)
        try:
            while True:
                await asyncio.sleep(100)
        except (KeyboardInterrupt):
            print("Closing Connection")
            self.pc.close()


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
    user = WebRTCuser()
    user.start()