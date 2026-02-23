import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import json
from loguru import logger
from typing import List, Dict, Any
import torch
import torch.nn as nn

import os
import cv2
import numpy as np

class LipSyncService:
    def __init__(self, avatar_path: str = None):
        # Set default avatar path if none is provided
        if avatar_path is None:
            avatar_path = r"C:\Users\hp\Downloads\advanced-avatar-main\000723.jpg"

        self.avatar = self._load_avatar(avatar_path)
        self.mouth_region = self._detect_mouth_region()
        self.viseme_shapes = self._load_viseme_shapes()
        self.prev_shape = None
        self.smoothing_factor = 0.3

    def _load_avatar(self, avatar_path: str) -> np.ndarray:
        """Load avatar image"""
        if os.path.exists(avatar_path): 
            img = cv2.imread(avatar_path)
            if img is not None:
                return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return self._create_animated_avatar()

    def _create_animated_avatar(self) -> np.ndarray:
        return np.zeros((256, 256, 3), dtype=np.uint8)

    def _detect_mouth_region(self):
        pass

    def _load_viseme_shapes(self):
        pass
    def _create_animated_avatar(self) -> np.ndarray:
        """Create a professional animated avatar"""
        img = Image.new('RGBA', (1024, 1024), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([200, 100, 824, 900], fill=(255, 220, 200, 255), outline=(100, 50, 30, 255), width=3)
        draw.ellipse([350, 300, 450, 400], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
        draw.ellipse([574, 300, 674, 400], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
        draw.ellipse([380, 340, 420, 380], fill=(0, 0, 0, 255))
        draw.ellipse([604, 340, 644, 380], fill=(0, 0, 0, 255))
        draw.arc([340, 250, 460, 320], start=30, end=150, fill=(0, 0, 0, 255), width=5)
        draw.arc([564, 250, 684, 320], start=30, end=150, fill=(0, 0, 0, 255), width=5)
        draw.polygon([500, 450, 520, 550, 480, 550], fill=(230, 190, 170, 255))
        self.mouth_region = (400, 600, 624, 700)
        return np.array(img)
        
    def _detect_mouth_region(self) -> tuple:
        """Detect mouth region in avatar"""
        return (400, 600, 624, 700) 
        
    def _load_viseme_shapes(self) -> Dict[str, Dict[str, float]]:
        """Load viseme to mouth shape mappings"""
        return {
            'viseme_silence': {'width': 0.2, 'height': 0.1, 'jaw': 0.0, 'round': 0.0, 'x_offset': 0, 'y_offset': 0},
            'viseme_aa': {'width': 0.8, 'height': 0.7, 'jaw': 0.8, 'round': 0.2, 'x_offset': 0, 'y_offset': 0},
            'viseme_ii': {'width': 0.5, 'height': 0.9, 'jaw': 0.3, 'round': 0.1, 'x_offset': 5, 'y_offset': -5},
            'viseme_uu': {'width': 0.6, 'height': 0.4, 'jaw': 0.4, 'round': 0.9, 'x_offset': 0, 'y_offset': 5},
            'viseme_e': {'width': 0.7, 'height': 0.5, 'jaw': 0.5, 'round': 0.3, 'x_offset': 0, 'y_offset': -3},
            'viseme_o': {'width': 0.6, 'height': 0.5, 'jaw': 0.5, 'round': 0.7, 'x_offset': 0, 'y_offset': 2},
            'viseme_k': {'width': 0.5, 'height': 0.3, 'jaw': 0.3, 'round': 0.2, 'x_offset': -2, 'y_offset': 0},
            'viseme_g': {'width': 0.5, 'height': 0.3, 'jaw': 0.3, 'round': 0.2, 'x_offset': 2, 'y_offset': 0},
            'viseme_t': {'width': 0.4, 'height': 0.2, 'jaw': 0.2, 'round': 0.1, 'x_offset': 3, 'y_offset': 0},
            'viseme_d': {'width': 0.4, 'height': 0.2, 'jaw': 0.2, 'round': 0.1, 'x_offset': -2, 'y_offset': 0},
            'viseme_n': {'width': 0.4, 'height': 0.2, 'jaw': 0.2, 'round': 0.1, 'x_offset': 0, 'y_offset': 0},
            'viseme_m': {'width': 0.4, 'height': 0.2, 'jaw': 0.2, 'round': 0.1, 'x_offset': 0, 'y_offset': 0},
            'viseme_p': {'width': 0.3, 'height': 0.1, 'jaw': 0.1, 'round': 0.1, 'x_offset': 0, 'y_offset': 2},
            'viseme_b': {'width': 0.3, 'height': 0.1, 'jaw': 0.1, 'round': 0.1, 'x_offset': 0, 'y_offset': 1},
            'viseme_s': {'width': 0.4, 'height': 0.1, 'jaw': 0.1, 'round': 0.1, 'x_offset': 0, 'y_offset': 1},
            'viseme_h': {'width': 0.5, 'height': 0.3, 'jaw': 0.3, 'round': 0.2, 'x_offset': 0, 'y_offset': 0}
        }
        
    def generate_frames(self, viseme_sequence: List[Dict], duration: float, fps: int = 30) -> List[np.ndarray]:
        """Generate frames with lip sync"""
        try:
            frames = []
            num_frames = int(duration * fps)
            
            for i in range(num_frames):
                current_time = i / fps
                viseme = self._get_active_viseme(viseme_sequence, current_time)
                
                frame = self._render_frame(viseme)
                frames.append(frame)
                
            return frames
            
        except Exception as e:
            logger.error(f"Frame generation error: {e}")
            return []
            
    def _get_active_viseme(self, viseme_sequence: List[Dict], time: float) -> Dict:
        """Get active viseme at given time with blending"""
        active_visemes = []
        
        for viseme in viseme_sequence:
            start = viseme['start']
            end = start + viseme.get('duration', 0.1)
            
            if start <= time <= end:
                # Calculate blend factor
                blend_duration = viseme.get('blend', 0.05)
                if time - start < blend_duration:
                    # Blending in
                    blend = (time - start) / blend_duration
                elif end - time < blend_duration:
                    # Blending out
                    blend = (end - time) / blend_duration
                else:
                    blend = 1.0
                    
                active_visemes.append({
                    'viseme': viseme['viseme'],
                    'blend': blend
                })
                
        if not active_visemes:
            return {'viseme': 'viseme_silence', 'blend': 1.0}
            
        # Return the one with highest blend
        return max(active_visemes, key=lambda x: x['blend'])
        
    def _render_frame(self, viseme_info: Dict) -> np.ndarray:
        """Render a single frame with mouth shape"""
        try:
            frame = self.avatar.copy()
            viseme_name = viseme_info['viseme']
            blend = viseme_info['blend']
            
            # Get mouth shape parameters
            shape = self.viseme_shapes.get(viseme_name, self.viseme_shapes['viseme_silence'])
            
            # Apply smoothing
            if self.prev_shape is None:
                self.prev_shape = shape
            else:
                # Interpolate shapes
                for key in shape:
                    if isinstance(shape[key], (int, float)):
                        shape[key] = self.prev_shape[key] * (1 - self.smoothing_factor) + shape[key] * self.smoothing_factor
                self.prev_shape = shape
                
            # Calculate mouth dimensions
            x1, y1, x2, y2 = self.mouth_region
            mouth_width = x2 - x1
            mouth_height = y2 - y1
            
            # Apply shape modifications
            new_width = int(mouth_width * shape['width'])
            new_height = int(mouth_height * shape['height'])
            x_offset = shape.get('x_offset', 0)
            y_offset = shape.get('y_offset', 0)
            
            # Center the mouth
            new_x1 = x1 + (mouth_width - new_width) // 2 + x_offset
            new_y1 = y1 + (mouth_height - new_height) // 2 + y_offset
            new_x2 = new_x1 + new_width
            new_y2 = new_y1 + new_height
            
            # Draw mouth with gradient
            img = Image.fromarray(frame)
            draw = ImageDraw.Draw(img, 'RGBA')
            
            # Draw multiple layers for depth
            for i in range(3):
                alpha = int(255 * (0.7 - i * 0.2) * blend)
                offset = i * 3
                draw.ellipse(
                    [new_x1 - offset, new_y1 - offset, new_x2 + offset, new_y2 + offset],
                    fill=(255, 100, 100, alpha)
                )
                
            # Add highlight
            highlight_y1 = new_y1 + new_height // 4
            highlight_y2 = new_y1 + new_height // 2
            draw.ellipse(
                [new_x1 + 5, highlight_y1, new_x2 - 5, highlight_y2],
                fill=(255, 255, 255, 100)
            )
            
            # Apply subtle blur
            img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            return np.array(img)
            
        except Exception as e:
            logger.error(f"Frame rendering error: {e}")
            return self.avatar