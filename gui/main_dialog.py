from aqt.qt import *
from aqt.utils import showInfo
from aqt import mw
import sys
from pathlib import Path

# Import our Gemini client
addon_dir = Path(__file__).parent.parent
sys.path.insert(0, str(addon_dir))
from utils.gemini_client import GeminiClient

class GeminiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gemini TTS & AI Assistant")
        self.setMinimumSize(500, 400)
        self.setup_ui()
        self.load_config()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # API Key section
        api_group = QGroupBox("API Configuration")
        api_layout = QVBoxLayout()
        
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("Enter your Google AI API key")
        self.api_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        api_button_layout = QHBoxLayout()
        self.save_api_btn = QPushButton("Save API Key")
        self.test_api_btn = QPushButton("Test Connection")
        api_button_layout.addWidget(self.save_api_btn)
        api_button_layout.addWidget(self.test_api_btn)
        
        api_layout.addWidget(QLabel("Google AI API Key:"))
        api_layout.addWidget(self.api_input)
        api_layout.addLayout(api_button_layout)
        api_group.setLayout(api_layout)
        
        # Text generation section
        text_group = QGroupBox("AI Text Generation")
        text_layout = QVBoxLayout()
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here...")
        self.prompt_input.setMaximumHeight(100)
        
        self.generate_btn = QPushButton("Generate Text")
        
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        
        text_layout.addWidget(QLabel("Prompt:"))
        text_layout.addWidget(self.prompt_input)
        text_layout.addWidget(self.generate_btn)
        text_layout.addWidget(QLabel("Result:"))
        text_layout.addWidget(self.result_output)
        text_group.setLayout(text_layout)
        
        # TTS section
        tts_group = QGroupBox("Text-to-Speech")
        tts_layout = QVBoxLayout()
        
        self.tts_input = QTextEdit()
        self.tts_input.setPlaceholderText("Enter text for TTS...")
        self.tts_input.setMaximumHeight(80)
        
        self.tts_btn = QPushButton("Generate TTS (Placeholder)")
        
        tts_layout.addWidget(QLabel("Text for TTS:"))
        tts_layout.addWidget(self.tts_input)
        tts_layout.addWidget(self.tts_btn)
        tts_group.setLayout(tts_layout)
        
        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: blue;")
        
        # Add to main layout
        layout.addWidget(api_group)
        layout.addWidget(text_group)
        layout.addWidget(tts_group)
        layout.addWidget(self.status_label)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        
        # Connect signals
        self.save_api_btn.clicked.connect(self.save_api_key)
        self.test_api_btn.clicked.connect(self.test_connection)
        self.generate_btn.clicked.connect(self.generate_text)
        self.tts_btn.clicked.connect(self.generate_tts)
    
    def load_config(self):
        """Load saved configuration"""
        config = mw.addonManager.getConfig(__name__)
        if config and config.get("api_key"):
            self.api_input.setText(config["api_key"])
            self.status_label.setText("API key loaded from config")
            self.status_label.setStyleSheet("color: green;")
    
    def save_api_key(self):
        """Save API key to config"""
        api_key = self.api_input.text().strip()
        if not api_key:
            showInfo("Please enter an API key")
            return
        
        config = mw.addonManager.getConfig(__name__) or {}
        config["api_key"] = api_key
        mw.addonManager.writeConfig(__name__, config)
        
        self.status_label.setText("API key saved successfully")
        self.status_label.setStyleSheet("color: green;")
        showInfo("API key saved successfully!")
    
    def test_connection(self):
        """Test Gemini API connection"""
        api_key = self.api_input.text().strip()
        if not api_key:
            showInfo("Please enter an API key first")
            return
        
        self.status_label.setText("Testing connection...")
        self.status_label.setStyleSheet("color: orange;")
        
        client = GeminiClient(api_key)
        success, message = client.test_connection()
        
        if success:
            self.status_label.setText("Connection successful!")
            self.status_label.setStyleSheet("color: green;")
            showInfo("Connection test successful!")
        else:
            self.status_label.setText(f"Connection failed: {message}")
            self.status_label.setStyleSheet("color: red;")
            showInfo(f"Connection test failed:\n{message}")
    
    def generate_text(self):
        """Generate text using Gemini"""
        api_key = self.api_input.text().strip()
        prompt = self.prompt_input.toPlainText().strip()
        
        if not api_key:
            showInfo("Please enter an API key first")
            return
        
        if not prompt:
            showInfo("Please enter a prompt")
            return
        
        self.status_label.setText("Generating text...")
        self.status_label.setStyleSheet("color: orange;")
        self.generate_btn.setEnabled(False)
        
        client = GeminiClient(api_key)
        result, error = client.generate_text(prompt)
        
        if result:
            self.result_output.setText(result)
            self.status_label.setText("Text generated successfully")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.result_output.setText(f"Error: {error}")
            self.status_label.setText("Text generation failed")
            self.status_label.setStyleSheet("color: red;")
        
        self.generate_btn.setEnabled(True)
    
    def generate_tts(self):
        """Generate TTS (placeholder)"""
        text = self.tts_input.toPlainText().strip()
        if not text:
            showInfo("Please enter text for TTS")
            return
        
        # Placeholder for TTS functionality
        showInfo(f"TTS placeholder: Would generate speech for:\n{text[:100]}...")
        self.status_label.setText("TTS functionality coming soon")
        self.status_label.setStyleSheet("color: blue;")

def show_gemini_dialog():
    """Show the Gemini dialog"""
    dialog = GeminiDialog(mw)
    dialog.exec()
