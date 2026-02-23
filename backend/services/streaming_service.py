import asyncio
import numpy as np
from aiortc import MediaStreamTrack
from av import VideoFrame
from loguru import logger

class VideoStreamTrack(MediaStreamTrack):
    """A video track that yields frames from an async generator."""
    kind = "video"

    def __init__(self, frame_generator, fps=30):
        super().__init__()
        self.frame_generator = frame_generator
        self.fps = fps
        self.counter = 0

    async def recv(self):
        # Wait for next frame
        try:
            frame = await self.frame_generator.__anext__()
        except StopAsyncIteration:
            # End of stream, send a black frame
            frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        except Exception as e:
            logger.error(f"Error in video stream: {e}")
            frame = np.zeros((1080, 1920, 3), dtype=np.uint8)

        # Convert to VideoFrame
        video_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        video_frame.pts = self.counter
        video_frame.time_base = 1 / self.fps
        self.counter += 1
        return video_frame


class StreamingService:
    def __init__(self):
        self.active_streams = {}

    async def start_stream(self, session_id, frame_generator):
        """Start streaming frames for a session"""
        track = VideoStreamTrack(frame_generator)
        self.active_streams[session_id] = track
        return track

    async def stop_stream(self, session_id):
        """Stop streaming for a session"""
        if session_id in self.active_streams:
            del self.active_streams[session_id]