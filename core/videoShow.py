import cv2
class VideoShow():

    def __init__(self) -> None:
        self.started = False
   
    async def addTrack(self, track):
        self.track = track
    

    async def start(self):
        # Read until video is completed
        while (True):
            
            # Capture frame-by-frame
            frame = await self.track.recv()
            if frame:
                # Display the resulting frame
                frame = frame.to_ndarray(format="bgr24")
                cv2.imshow('Video', frame)
                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            # Break the loop
            else:
                break
        # When everything done, release the video capture object
        # Closes all the frames
        cv2.destroyAllWindows()