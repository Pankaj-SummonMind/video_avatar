import asyncio
import io
import hashlib
import os
import json
from pathlib import Path
from gtts import gTTS
import aiohttp
import numpy as np
from loguru import logger
from typing import Tuple, Optional
import azure.cognitiveservices.speech as speechsdk

class TextToSpeechService:
    def __init__(self, engine="azure", language="hi-IN", voice="hi-IN-SwaraNeural"):
        self.engine = engine
        self.language = language
        self.voice = voice
        self.cache_dir = Path("cache/tts")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Azure if needed
        if engine == "azure":
            self.speech_config = speechsdk.SpeechConfig(
                subscription=os.getenv("AZURE_SPEECH_KEY"),
                region=os.getenv("AZURE_SPEECH_REGION")
            )
            self.speech_config.speech_synthesis_voice_name = voice
            
    async def synthesize(self, text: str) -> Tuple[Optional[bytes], Optional[list]]:
        """Synthesize speech from text with timings"""
        try:
            # Check cache
            cache_key = hashlib.md5(f"{text}_{self.voice}".encode()).hexdigest()
            cache_path = self.cache_dir / f"{cache_key}.mp3"
            timing_path = self.cache_dir / f"{cache_key}.json"
            
            if cache_path.exists() and timing_path.exists():
                with open(cache_path, 'rb') as f:
                    audio_data = f.read()
                with open(timing_path, 'r') as f:
                    timings = json.load(f)
                return audio_data, timings
                
            # Generate speech based on engine
            if self.engine == "azure":
                audio_data, timings = await self._azure_tts(text)
            elif self.engine == "elevenlabs":
                audio_data, timings = await self._elevenlabs_tts(text)
            else:
                audio_data, timings = await self._google_tts(text)
                
            # Cache results
            if audio_data:
                with open(cache_path, 'wb') as f:
                    f.write(audio_data)
                with open(timing_path, 'w') as f:
                    json.dump(timings, f)
                    
            return audio_data, timings
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return None, None
            
    async def _google_tts(self, text: str) -> Tuple[Optional[bytes], Optional[list]]:
        """Google TTS implementation"""
        try:
            tts = gTTS(text=text, lang=self.language[:2], slow=False)
            
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            audio_data = audio_bytes.read()
            
            # Generate approximate timings
            words = text.split()
            word_duration = len(audio_data) / (len(words) * 16000)
            timings = []
            current_time = 0
            
            for word in words:
                timings.append({
                    'word': word,
                    'start': current_time,
                    'end': current_time + word_duration,
                    'phonemes': self._word_to_phonemes(word)
                })
                current_time += word_duration
                
            return audio_data, timings
            
        except Exception as e:
            logger.error(f"Google TTS error: {e}")
            return None, None
            
    async def _azure_tts(self, text: str) -> Tuple[Optional[bytes], Optional[list]]:
        """Azure TTS with viseme events"""
        try:
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
            
            # Enable viseme events
            viseme_data = []
            
            def viseme_callback(evt):
                viseme_data.append({
                    'viseme_id': evt.viseme_id,
                    'audio_offset': evt.audio_offset / 10000000,  # Convert to seconds
                    'animation': evt.animation
                })
                
            synthesizer.viseme_received.connect(viseme_callback)
            
            # Synthesize
            result = await synthesizer.speak_text_async(text)
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                audio_data = result.audio_data
                
                # Process visemes
                timings = []
                for viseme in viseme_data:
                    timings.append({
                        'viseme': f"viseme_{viseme['viseme_id']}",
                        'start': viseme['audio_offset'],
                        'duration': 0.1,  # Default duration
                        'blend': 0.2
                    })
                    
                return audio_data, timings
                
        except Exception as e:
            logger.error(f"Azure TTS error: {e}")
            return None, None
            
    async def _elevenlabs_tts(self, text: str) -> Tuple[Optional[bytes], Optional[list]]:
        """ElevenLabs TTS implementation"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
                    headers={
                        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
                        "Content-Type": "application/json"
                    },
                    json={
                        "text": text,
                        "voice_settings": {
                            "stability": 0.5,
                            "similarity_boost": 0.5
                        }
                    }
                ) as response:
                    audio_data = await response.read()
                    
            # ElevenLabs doesn't provide timings, so approximate
            words = text.split()
            word_duration = len(audio_data) / (len(words) * 16000)
            timings = []
            current_time = 0
            
            for word in words:
                timings.append({
                    'word': word,
                    'start': current_time,
                    'end': current_time + word_duration,
                    'phonemes': self._word_to_phonemes(word)
                })
                current_time += word_duration
                
            return audio_data, timings
            
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            return None, None
            
    def _word_to_phonemes(self, word: str) -> list:
        """Convert word to phoneme sequence (simplified)"""
        # In production, use a proper phonemizer like gruut or espeak
        phonemes = []
        for char in word.lower():
            if char in 'aeiou':
                phonemes.append({
                    'phoneme': 'V' + char,
                    'duration': 0.1
                })
            elif char.isalpha():
                phonemes.append({
                    'phoneme': 'C' + char,
                    'duration': 0.08
                })
        return phonemes