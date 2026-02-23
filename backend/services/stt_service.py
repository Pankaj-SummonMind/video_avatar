import asyncio
import speech_recognition as sr
import io
import wave
import numpy as np
from loguru import logger
from typing import Optional, AsyncGenerator
import aiohttp
import json

class SpeechToTextService:
    def __init__(self, engine="google", language="hi-IN"):
        self.engine = engine
        self.language = language
        self.recognizer = sr.Recognizer()
        
        # Adjust for ambient noise
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 3000
        
    async def convert_stream(self, audio_generator: AsyncGenerator[bytes, None]) -> AsyncGenerator[str, None]:
        """Convert audio stream to text in real-time"""
        async for audio_chunk in audio_generator:
            text = await self._convert_chunk(audio_chunk)
            if text:
                yield text
                
    async def _convert_chunk(self, audio_data: bytes) -> Optional[str]:
        """Convert single audio chunk to text"""
        try:
            # Convert to WAV format
            wav_data = self._convert_to_wav(audio_data)
            
            # Use speech recognition
            with sr.AudioFile(io.BytesIO(wav_data)) as source:
                audio = self.recognizer.record(source)
                
            if self.engine == "google":
                text = self.recognizer.recognize_google(audio, language=self.language)
            elif self.engine == "azure":
                text = await self._azure_speech_to_text(wav_data)
            elif self.engine == "whisper":
                text = await self._whisper_stt(wav_data)
            else:
                text = self.recognizer.recognize_google(audio, language=self.language)
                
            logger.info(f"STT: {text}")
            return text
            
        except sr.UnknownValueError:
            # No speech detected
            return None
        except Exception as e:
            logger.error(f"STT error: {e}")
            return None
            
    def _convert_to_wav(self, audio_data: bytes, sample_rate=16000) -> bytes:
        """Convert raw audio to WAV format"""
        try:
            # Assuming audio_data is in appropriate format
            # In production, you'd use proper audio conversion
            wav_io = io.BytesIO()
            with wave.open(wav_io, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data)
            return wav_io.getvalue()
        except Exception as e:
            logger.error(f"Audio conversion error: {e}")
            return audio_data
            
    async def _azure_speech_to_text(self, audio_data: bytes) -> Optional[str]:
        """Use Azure Cognitive Services for STT"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            speech_config = speechsdk.SpeechConfig(
                subscription=settings.AZURE_SPEECH_KEY,
                region=settings.AZURE_SPEECH_REGION
            )
            speech_config.speech_recognition_language = self.language
            
            audio_input = speechsdk.AudioDataStream(audio_data)
            recognizer = speechsdk.SpeechRecognizer(speech_config, audio_input)
            
            result = await recognizer.recognize_once_async()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return result.text
                
        except Exception as e:
            logger.error(f"Azure STT error: {e}")
            return None
            
    async def _whisper_stt(self, audio_data: bytes) -> Optional[str]:
        """Use OpenAI Whisper for STT"""
        try:
            import openai
            
            # Convert to format Whisper expects
            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.wav"
            
            response = await openai.Audio.atranscribe(
                model="whisper-1",
                file=audio_file,
                language=self.language[:2]  # 'hi' for Hindi
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Whisper STT error: {e}")
            return None