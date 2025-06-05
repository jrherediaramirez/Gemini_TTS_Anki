from aqt.qt import *
from aqt.utils import showInfo
from aqt import mw
import sys
from pathlib import Path

# Make Gemini client importable
addon_dir = Path(__file__).parent.parent
sys.path.insert(0, str(addon_dir))


class GeminiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gemini TTS & AI Assistant")
        self.setMinimumSize(500, 400)
        self.setup_ui()
        self.load_config()

    # -----------------------------
    # UI SETUP
    # -----------------------------
    def setup_ui(self):
        layout = QVBoxLayout()

        # --- API Key section ---
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

        # --- Text generation section ---
        text_group = QGroupBox("AI Text Generation")
        text_layout = QVBoxLayout()

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here…")
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

        # --- TTS section ---
        tts_group = QGroupBox("Text-to-Speech")
        tts_layout = QVBoxLayout()

        self.tts_input = QTextEdit()
        self.tts_input.setPlaceholderText("Enter text for TTS…")
        self.tts_input.setMaximumHeight(80)

        self.tts_btn = QPushButton("Generate Speech")

        tts_layout.addWidget(QLabel("Text for TTS:"))
        tts_layout.addWidget(self.tts_input)
        tts_layout.addWidget(self.tts_btn)
        tts_group.setLayout(tts_layout)

        # --- Status label ---
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: blue;")

        # Assemble main layout
        layout.addWidget(api_group)
        layout.addWidget(text_group)
        layout.addWidget(tts_group)
        layout.addWidget(self.status_label)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)

        # Signal wiring
        self.save_api_btn.clicked.connect(self.save_api_key)
        self.test_api_btn.clicked.connect(self.test_connection)
        self.generate_btn.clicked.connect(self.generate_text)
        self.tts_btn.clicked.connect(self.generate_tts)

    # -----------------------------
    # CONFIG HANDLING
    # -----------------------------
    def load_config(self):
        """Load saved configuration"""
        addon_name = Path(__file__).parent.parent.name
        config = mw.addonManager.getConfig(addon_name)
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

        addon_name = Path(__file__).parent.parent.name
        config = mw.addonManager.getConfig(addon_name) or {}
        config["api_key"] = api_key
        mw.addonManager.writeConfig(addon_name, config)

        self.status_label.setText("API key saved successfully")
        self.status_label.setStyleSheet("color: green;")
        showInfo("API key saved successfully!")

    # -----------------------------
    # GEMINI CONNECTION
    # -----------------------------
    def test_connection(self):
        """Test Gemini API connection"""
        try:
            api_key = self.api_input.text().strip()
            if not api_key:
                showInfo("Please enter an API key first")
                return

            self.status_label.setText("Testing connection…")
            self.status_label.setStyleSheet("color: orange;")

            from utils.gemini_client import GeminiClient

            client = GeminiClient(api_key)
            success, message = client.test_connection()

            if success:
                self.status_label.setText("Connection successful!")
                self.status_label.setStyleSheet("color: green;")
                showInfo("Connection test successful!")
            else:
                msg = message or "Unknown connection error"
                self.status_label.setText(f"Connection failed: {msg}")
                self.status_label.setStyleSheet("color: red;")
                showInfo(f"Connection test failed:\n{msg}")

        except Exception as e:
            self.status_label.setText("Connection test failed")
            self.status_label.setStyleSheet("color: red;")
            showInfo(f"Connection test error:\n{str(e)}")
            print(f"GeminiTTS Connection Error: {e}")

    # -----------------------------
    # TEXT GENERATION
    # -----------------------------
    def generate_text(self):
        """Generate text using Gemini"""
        try:
            api_key = self.api_input.text().strip()
            prompt = self.prompt_input.toPlainText().strip()

            if not api_key:
                showInfo("Please enter an API key first")
                return

            if not prompt:
                showInfo("Please enter a prompt")
                return

            self.status_label.setText("Generating text…")
            self.status_label.setStyleSheet("color: orange;")
            self.generate_btn.setEnabled(False)

            from utils.gemini_client import GeminiClient

            client = GeminiClient(api_key)
            result, error = client.generate_text(prompt)

            if result and result.strip():
                self.result_output.setText(str(result))
                self.status_label.setText("Text generated successfully")
                self.status_label.setStyleSheet("color: green;")
            else:
                error_msg = error or "No response received"
                self.result_output.setText(f"Error: {error_msg}")
                self.status_label.setText("Text generation failed")
                self.status_label.setStyleSheet("color: red;")

        except Exception as e:
            self.result_output.setText(f"Unexpected error: {str(e)}")
            self.status_label.setText("Text generation failed")
            self.status_label.setStyleSheet("color: red;")
            print(f"GeminiTTS GUI Error: {e}")
        finally:
            self.generate_btn.setEnabled(True)

    # -----------------------------
    # TTS GENERATION
    # -----------------------------
    def generate_tts(self):
        """Generate TTS using Google Cloud TTS"""
        try:
            api_key = self.api_input.text().strip()
            text = self.tts_input.toPlainText().strip()

            if not api_key:
                showInfo("Please enter an API key first")
                return

            if not text:
                showInfo("Please enter text for TTS")
                return

            if len(text) > 5000:
                showInfo("Text too long. Please limit to 5000 characters.")
                return

            self.status_label.setText("Generating speech…")
            self.status_label.setStyleSheet("color: orange;")
            self.tts_btn.setEnabled(False)

            from utils.gemini_client import GeminiClient

            client = GeminiClient(api_key)
            audio_data, error = client.generate_tts_audio(text)

            if audio_data:
                import tempfile
                import os

                temp_dir = tempfile.gettempdir()
                audio_file = os.path.join(temp_dir, "anki_tts_output.mp3")

                with open(audio_file, "wb") as f:
                    f.write(audio_data)

                self.status_label.setText("Speech generated successfully!")
                self.status_label.setStyleSheet("color: green;")

                try:
                    import subprocess
                    import platform

                    system = platform.system()
                    if system == "Windows":
                        os.startfile(audio_file)
                    elif system == "Darwin":  # macOS
                        subprocess.call(["open", audio_file])
                    else:  # Linux
                        subprocess.call(["xdg-open", audio_file])

                    showInfo(
                        f"Speech generated and saved!\nFile: {audio_file}\n\nAttempting to play audio…"
                    )

                except Exception as play_error:
                    showInfo(
                        f"Speech generated and saved to:\n{audio_file}\n\nCouldn't auto-play: {play_error}"
                    )
            else:
                error_msg = error or "Unknown TTS error"
                self.status_label.setText("TTS generation failed")
                self.status_label.setStyleSheet("color: red;")
                showInfo(f"TTS generation failed:\n{error_msg}")

        except Exception as e:
            self.status_label.setText("TTS generation failed")
            self.status_label.setStyleSheet("color: red;")
            showInfo(f"TTS error:\n{str(e)}")
            print(f"GeminiTTS GUI TTS Error: {e}")
        finally:
            self.tts_btn.setEnabled(True)


# --------------------------------------------------
# PUBLIC ENTRY POINT
# --------------------------------------------------

def show_gemini_dialog():
    """Show the Gemini dialog"""
    dialog = GeminiDialog(mw)
    dialog.exec()
