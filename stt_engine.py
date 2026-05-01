import whisper
import warnings

# Suppress FP16 warnings on CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

class STTEngine:
    def __init__(self, model_size="base"):
        self.model_size = model_size
        self.model = None

    def load_model(self):
        print(f"Loading Whisper model ({self.model_size})...")
        self.model = whisper.load_model(self.model_size)
        print("Whisper model loaded.")

    def transcribe(self, audio_file_path):
        if self.model is None:
            self.load_model()
            
        print(f"Transcribing {audio_file_path}...")
        result = self.model.transcribe(audio_file_path)
        return result["text"].strip()
