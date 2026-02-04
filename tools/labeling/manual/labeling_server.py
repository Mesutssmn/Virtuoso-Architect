"""
Flask Server for MIDI Labeling Tool
Provides REST API for the web interface.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from label_manager import LabelManager

app = Flask(__name__)
CORS(app)  # Enable CORS for local development

import argparse
from tools.labeling.config import DEFAULT_CONFIG

# Parse arguments
parser = argparse.ArgumentParser(description="MIDI Labeling Server")
parser.add_argument("--config", default=DEFAULT_CONFIG, help="Label configuration (4_labels or 5_labels)")
args, unknown = parser.parse_known_args()

# Initialize label manager
project_root = Path(__file__).parent.parent.parent.parent  # Go up 4 levels to root
features_csv = project_root / "data" / "processed" / "features_all.csv"
# Labels file specific to config
labels_csv = project_root / "data" / "processed" / "labels" / f"manual_{args.config}.csv"
progress_file = project_root / "data" / "processed" / "labels" / f"progress_{args.config}.json"

print(f"\n🚀 Starting Server with Config: {args.config}")
print(f"📁 Labels File: {labels_csv}")

manager = LabelManager(
    str(features_csv),
    str(labels_csv),
    str(progress_file),
    config_name=args.config
)


@app.route('/')
def index():
    """Serve the labeling interface."""
    return send_from_directory(str(Path(__file__).parent), 'labeling_interface.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get labeling configuration."""
    return jsonify(manager.get_config())


@app.route('/api/current', methods=['GET'])
def get_current():
    """Get current file to label."""
    file_info = manager.get_current_file()
    
    if file_info is None:
        return jsonify({
            'error': 'All files have been labeled! 🎉',
            'completed': True
        })
    
    return jsonify(file_info)


@app.route('/api/label', methods=['POST'])
def save_label():
    """Save a label for the current file."""
    data = request.json
    filename = data.get('filename')
    label = data.get('label')
    
    if filename is None or label is None:
        return jsonify({'success': False, 'error': 'Missing filename or label'}), 400
    
    success = manager.save_label(filename, label)
    
    return jsonify({'success': success})


@app.route('/api/next', methods=['GET'])
def next_file():
    """Move to next file."""
    file_info = manager.next_file()
    
    if file_info is None:
        return jsonify({
            'error': 'All files have been labeled! 🎉',
            'completed': True
        })
    
    return jsonify(file_info)


@app.route('/api/previous', methods=['GET'])
def previous_file():
    """Move to previous file."""
    file_info = manager.previous_file()
    
    if file_info is None:
        return jsonify({'error': 'Already at first file'}), 400
    
    return jsonify(file_info)


@app.route('/api/jump/<int:index>', methods=['GET'])
def jump_to_index(index):
    """Jump to specific file index."""
    file_info = manager.jump_to_index(index)
    
    if file_info is None:
        return jsonify({'error': 'Invalid index'}), 400
    
    return jsonify(file_info)


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get labeling statistics."""
    stats = manager.get_statistics()
    return jsonify(stats)


@app.route('/api/midi/<path:filename>', methods=['GET'])
def get_midi_file(filename):
    """Serve MIDI file for playback."""
    midi_dir = project_root / "data" / "raw"
    return send_from_directory(str(midi_dir), filename)


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎹 MIDI LABELING TOOL - SERVER STARTING")
    print("="*70)
    print(f"\n📁 Features: {features_csv}")
    print(f"📁 Labels: {labels_csv}")
    print(f"📁 Progress: {progress_file}")
    print(f"\n🌐 Open in browser: http://localhost:5000")
    print(f"\n⌨️  Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
