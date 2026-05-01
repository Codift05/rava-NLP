import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QTextEdit, QProgressBar, QSplitter)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from audio_capture import AudioRecorder
from stt_engine import STTEngine
from summarizer import SummarizerEngine

class AIWorker(QThread):
    finished = pyqtSignal(str, str)
    progress = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, audio_file):
        super().__init__()
        self.audio_file = audio_file
        self.stt = STTEngine()
        self.summarizer = SummarizerEngine()

    def run(self):
        try:
            self.progress.emit("Loading Whisper model...")
            self.stt.load_model()
            
            self.progress.emit("Transcribing audio...")
            transcription = self.stt.transcribe(self.audio_file)
            
            self.progress.emit("Loading Summarizer model...")
            self.summarizer.load_model()
            
            self.progress.emit("Summarizing text...")
            summary = self.summarizer.summarize(transcription)
            
            self.finished.emit(transcription, summary)
            
            # Clean up temp file
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)
                
        except Exception as e:
            self.error.emit(str(e))

class RavaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.recorder = AudioRecorder()
        self.initUI()
        self.populate_devices()
        
    def initUI(self):
        self.setWindowTitle("Rava - Recap Voice Analysis Assistant")
        self.resize(800, 600)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Header
        header_label = QLabel("Rava: Meeting Summarizer")
        header_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.device_combo = QComboBox()
        controls_layout.addWidget(QLabel("Input Device:"))
        controls_layout.addWidget(self.device_combo, stretch=1)
        
        self.btn_start = QPushButton("Start Recording")
        self.btn_start.clicked.connect(self.start_recording)
        self.btn_start.setStyleSheet("background-color: #ff4d4d; color: white; font-weight: bold; padding: 5px;")
        controls_layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton("Stop & Process")
        self.btn_stop.clicked.connect(self.stop_recording)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 5px;")
        controls_layout.addWidget(self.btn_stop)
        
        main_layout.addLayout(controls_layout)
        
        # Status Bar
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("color: gray;")
        main_layout.addWidget(self.status_label)
        
        # Output Area
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Transcription
        trans_widget = QWidget()
        trans_layout = QVBoxLayout(trans_widget)
        trans_layout.setContentsMargins(0, 0, 0, 0)
        trans_label = QLabel("Transcription:")
        trans_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.text_transcription = QTextEdit()
        self.text_transcription.setReadOnly(True)
        trans_layout.addWidget(trans_label)
        trans_layout.addWidget(self.text_transcription)
        
        # Summary
        sum_widget = QWidget()
        sum_layout = QVBoxLayout(sum_widget)
        sum_layout.setContentsMargins(0, 0, 0, 0)
        sum_label = QLabel("Summary:")
        sum_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.text_summary = QTextEdit()
        self.text_summary.setReadOnly(True)
        self.text_summary.setStyleSheet("background-color: #f0f8ff;")
        sum_layout.addWidget(sum_label)
        sum_layout.addWidget(self.text_summary)
        
        splitter.addWidget(trans_widget)
        splitter.addWidget(sum_widget)
        main_layout.addWidget(splitter, stretch=1)
        
    def populate_devices(self):
        devices = self.recorder.get_devices()
        for idx, name in devices:
            self.device_combo.addItem(name, userData=idx)
            
    def start_recording(self):
        device_idx = self.device_combo.currentData()
        self.recorder.start_recording(device_index=device_idx)
        
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.status_label.setText("Status: Recording...")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.text_transcription.clear()
        self.text_summary.clear()
        
    def stop_recording(self):
        self.status_label.setText("Status: Saving audio...")
        self.status_label.setStyleSheet("color: orange; font-weight: bold;")
        self.btn_stop.setEnabled(False)
        
        # Stop recording and get file
        audio_file = self.recorder.stop_recording("meeting_audio.wav")
        
        if audio_file:
            self.process_audio(audio_file)
        else:
            self.status_label.setText("Status: Error saving audio.")
            self.btn_start.setEnabled(True)
            
    def process_audio(self, audio_file):
        self.status_label.setText("Status: Starting AI processing...")
        
        self.worker = AIWorker(audio_file)
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.processing_finished)
        self.worker.error.connect(self.processing_error)
        self.worker.start()
        
    def update_status(self, msg):
        self.status_label.setText(f"Status: {msg}")
        self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        
    def processing_finished(self, trans, summary):
        self.text_transcription.setPlainText(trans)
        self.text_summary.setPlainText(summary)
        self.status_label.setText("Status: Processing Complete")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.btn_start.setEnabled(True)
        
    def processing_error(self, err_msg):
        self.status_label.setText(f"Status: Error - {err_msg}")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.btn_start.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = RavaApp()
    window.show()
    sys.exit(app.exec())
