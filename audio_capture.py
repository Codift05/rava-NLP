import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import threading
import queue
import time

class AudioRecorder:
    def __init__(self, samplerate=16000, channels=1):
        self.samplerate = samplerate
        self.channels = channels
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.recording_thread = None

    def get_devices(self):
        devices = sd.query_devices()
        input_devices = []
        for idx, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                input_devices.append((idx, device['name']))
        return input_devices

    def _callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(f"Audio Callback Status: {status}", flush=True)
        self.audio_queue.put(indata.copy())

    def start_recording(self, device_index=None):
        if self.is_recording:
            return

        self.is_recording = True
        self.audio_queue = queue.Queue() # Reset queue
        
        def record():
            try:
                with sd.InputStream(samplerate=self.samplerate, 
                                    device=device_index,
                                    channels=self.channels, 
                                    callback=self._callback):
                    while self.is_recording:
                        time.sleep(0.1)
            except Exception as e:
                print(f"Error recording audio: {e}")
                self.is_recording = False

        self.recording_thread = threading.Thread(target=record)
        self.recording_thread.start()

    def stop_recording(self, filename="temp_recording.wav"):
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join()
        
        audio_data = []
        while not self.audio_queue.empty():
            audio_data.append(self.audio_queue.get())
        
        if audio_data:
            audio_data = np.concatenate(audio_data, axis=0)
            wav.write(filename, self.samplerate, audio_data)
            return filename
        return None
