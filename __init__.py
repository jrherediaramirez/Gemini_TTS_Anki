"""
Gemini TTS Add-on for Anki
Provides AI text generation and TTS using Google Gemini API
"""

import sys
from pathlib import Path

# Add lib folder to Python path
addon_path = Path(__file__).parent
lib_path = addon_path / "lib"
if lib_path.exists() and str(lib_path) not in sys.path:
    sys.path.insert(0, str(lib_path))

# Anki imports
from aqt import mw, gui_hooks
from aqt.utils import showInfo, qconnect
from aqt.qt import QAction

def check_first_run():
    """Check if this is first run and prompt for API key"""
    config = mw.addonManager.getConfig(__name__)
    if not config or not config.get("api_key"):
        showInfo(
            "Welcome to Gemini TTS!\n\n"
            "This is your first time running the add-on.\n"
            "You'll need a Google AI API key to use this add-on.\n\n"
            "Get your free API key at:\n"
            "https://aistudio.google.com/app/apikey\n\n"
            "Click 'Tools > Gemini TTS' to configure your API key."
        )

def show_gemini_dialog():
    """Show the main Gemini dialog"""
    try:
        from gui.main_dialog import show_gemini_dialog as show_dialog
        show_dialog()
    except Exception as e:
        showInfo(f"Error opening Gemini dialog:\n{str(e)}")
        print(f"Gemini dialog error: {e}")

def init_addon():
    """Initialize the add-on"""
    try:
        # Add menu item
        action = QAction("Gemini TTS", mw)
        qconnect(action.triggered, show_gemini_dialog)
        mw.form.menuTools.addAction(action)
        
        # Check for first run after Anki is fully loaded
        gui_hooks.main_window_did_init.append(lambda: check_first_run())
        
        print("Gemini TTS add-on initialized successfully")
        
    except Exception as e:
        print(f"Error initializing Gemini TTS add-on: {e}")
        showInfo(f"Error initializing Gemini TTS add-on:\n{str(e)}")

# Initialize the add-on
init_addon()
