import cv2
from mlfApi import process
import threading
import time


class VideoBuffer():
    def __init__(self) -> None:
        self.started = False
        self.frame = None

    async def addTrack(self, track):
        self.track = track

    async def start(self, showVideo= False):
        self.started = True
        if showVideo:
            self.videoShow = VideoShow(self)
            self.videoShow.start()
        while (self.started):
            self.frame = await self.track.recv()
        self.showVideo.stop()
    
    def stop(self):
        self.started = False
    
    def getCurrentFrame(self):
        return self.frame

class VideoShow():

    def __init__(self, buffer) -> None:
        self.buffer = buffer

    def showLoop(self):
        # Read until video is completed
        self.show = True
        time.sleep(1)
        while (self.show):
            # Capture frame-by-frame
            frame = self.buffer.getCurrentFrame()
            if frame:
                # Display the resulting frame
                frame = frame.to_ndarray(format="bgr24")
                frame = process(frame)
                cv2.imshow('Video', frame)
                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            # Break the loop
            else: 
                time.sleep(1)
        # When everything done, release the video capture object
        # Closes all the frames
        cv2.destroyAllWindows()

    def start(self):
        self.cameraThread = threading.Thread(target=self.showLoop, args=())
        self.cameraThread.start()
    
    def stop(self):
        self.show = False
        self.cameraThread.join()
        