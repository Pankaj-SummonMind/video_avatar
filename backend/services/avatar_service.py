import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip
import asyncio
import uuid
from pathlib import Path
from loguru import logger
from typing import List, Optional
import aiofiles

class AvatarRenderService:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    async def render_video(
        self, 
        frames: List[np.ndarray], 
        audio_data: bytes,
        fps: int = 30,
        quality: str = "high"
    ) -> Optional[str]:
        """Render video from frames and audio"""
        try:
            video_id = str(uuid.uuid4())
            video_path = self.output_dir / f"{video_id}.mp4"
            temp_audio = self.output_dir / f"{video_id}_audio.mp3"
            
            # Save audio temporarily
            async with aiofiles.open(temp_audio, 'wb') as f:
                await f.write(audio_data)
                
            # Convert frames to RGB
            rgb_frames = []
            for frame in frames:
                if len(frame.shape) == 3:
                    if frame.shape[2] == 4:  # RGBA
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
                    elif frame.shape[2] == 3:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_frames.append(frame)
                
            # Create video clip
            clip = ImageSequenceClip(rgb_frames, fps=fps)
            
            # Set quality parameters
            if quality == "high":
                bitrate = "5000k"
                codec = "libx264"
            else:
                bitrate = "2000k"
                codec = "libx264"
                
            # Add audio
            audio_clip = AudioFileClip(str(temp_audio))
            final_clip = clip.set_audio(audio_clip)
            
            # Write video
            final_clip.write_videofile(
                str(video_path),
                codec=codec,
                audio_codec='aac',
                bitrate=bitrate,
                preset='medium',
                fps=fps,
                logger=None
            )
            
            # Cleanup
            temp_audio.unlink()
            
            logger.info(f"Video rendered: {video_path}")
            return str(video_path)
            
        except Exception as e:
            logger.error(f"Video rendering error: {e}")
            if temp_audio.exists():
                temp_audio.unlink()
            return None
            
    async def render_stream(self, frames: List[np.ndarray], fps: int = 30):
        """Render video stream (for WebRTC)"""
        for frame in frames:
            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            yield buffer.tobytes()
            
    async def add_watermark(self, video_path: str, watermark_text: str = "AI Avatar") -> str:
        """Add watermark to video"""
        try:
            video = VideoFileClip(video_path)
            
            # Create watermark
            from moviepy.video.VideoClip import TextClip
            from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
            
            watermark = TextClip(
                watermark_text,
                fontsize=30,
                color='white',
                font='Arial',
                stroke_color='black',
                stroke_width=1
            ).set_position(('right', 'bottom')).set_duration(video.duration)
            
            # Composite
            final = CompositeVideoClip([video, watermark])
            
            # Save
            watermarked_path = video_path.replace('.mp4', '_watermarked.mp4')
            final.write_videofile(watermarked_path, codec='libx264', audio_codec='aac')
            
            return watermarked_path
            
        except Exception as e:
            logger.error(f"Watermark error: {e}")
            return video_path