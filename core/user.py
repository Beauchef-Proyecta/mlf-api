import asyncio
from aiortc import (
    RTCPeerConnection,
    RTCConfiguration
)
from videoShow import VideoShow
from signaling import SignalingServer
from aiortc.contrib.media import MediaStreamTrack
from aiortc.contrib.signaling import BYE, add_signaling_arguments, create_signaling
from av import VideoFrame





class SimpleVideoTrack(MediaStreamTrack):

    kind = "video"

    def __init__(self, track):
        super().__init__()  # don't forget this!
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        return frame




async def run(pc, videoShow: VideoShow, signaling):

    @pc.on("track")
    async def on_track(track):
        print("hola")
        print("Receiving %s" % track.kind)
        if track.kind == 'video':
            await videoShow.addTrack(SimpleVideoTrack(track))
            if (not videoShow.started):
                await videoShow.start()

        
    # send offer
    pc.addTransceiver('video', direction = 'recvonly')
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    response = await signaling.postOffer(pc.localDescription)
    await pc.setRemoteDescription(response)
    try:
        while True:
            await asyncio.sleep(100)
    except (KeyboardInterrupt):
        print("Closing Connection")
        pc.close()


if __name__ == "__main__":

    # create signaling and peer connection
    signaling = SignalingServer()
    pc = RTCPeerConnection(configuration=RTCConfiguration(iceServers=[]))

    videoShow = VideoShow()

    # run event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            run(
                pc=pc,
                videoShow=videoShow,
                signaling=signaling
            )
        )
    except KeyboardInterrupt:
        pass
    finally:
        # cleanup
        loop.run_until_complete(pc.close())
