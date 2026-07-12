# Vehicle Traffic Counter

Vehicle Traffic Counter is a PyQt6-based desktop application for loading and reviewing traffic video footage.

## Requirements
- Python 3.10 or newer
- PyQt6
- python-vlc

## Setup
1. Create and activate a virtual environment:
   - Windows PowerShell:
     - `py -3 -m venv venv`
     - `.\venv\Scripts\Activate.ps1`
2. Install dependencies:
   - `pip install --upgrade pip`
   - `pip install -r requirements.txt`
3. Start the application:
   - `python main.py`

## Notes
- The UI is generated from the Qt Designer file in [app/ui/main_window.ui](app/ui/main_window.ui).
- If you run the app in a headless environment, set `QT_QPA_PLATFORM=offscreen` before launching it.
- The application currently opens the main window and is ready for video-loading features to be connected.
