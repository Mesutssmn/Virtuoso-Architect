"""
Start Labeling Tool
Quick script to launch the labeling interface.
"""

import sys
import webbrowser
import time
from pathlib import Path
from threading import Timer

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def open_browser():
    """Open browser after a short delay."""
    webbrowser.open('http://localhost:5000')

def main():
    print("\n" + "="*70)
    print("🎹 MIDI LABELING TOOL - QUICK START")
    print("="*70)
    print("\n📋 Instructions:")
    print("  1. The server will start in a moment")
    print("  2. Your browser will open automatically")
    print("  3. Use keyboard shortcuts (1-5) to label files")
    print("  4. Press Ctrl+C to stop when done")
    print("\n" + "="*70 + "\n")
    
    # Open browser after 2 seconds
    Timer(2.0, open_browser).start()
    
    # Import and run server (using absolute path)
    tools_dir = Path(__file__).parent
    server_path = tools_dir / "labeling_server.py"
    
    # Load the server module
    import importlib.util
    spec = importlib.util.spec_from_file_location("labeling_server", server_path)
    server_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(server_module)
    
    # Run the app
    server_module.app.run(debug=False, port=5000, host='0.0.0.0')

if __name__ == "__main__":
    main()
