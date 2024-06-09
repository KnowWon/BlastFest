from flask import Flask, render_template, jsonify
import subprocess
import time
import numpy as np
import wave

app = Flask(__name__)

# Remaining code...

@app.route('/audio_levels')
def audio_levels():
    try:
        # Capture audio using jack_capture
        subprocess.run(['jack_capture', '-d', '1', '-c', '2', 'input2.wav'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Get audio levels from the captured file
        peak_left, peak_right = get_audio_levels('input2.wav')

        print(f"Received audio levels from capture_audio_levels.py - Peak Left: {peak_left}, Peak Right: {peak_right}")

        if peak_left is not None and peak_right is not None:
            return jsonify({'peak_left': peak_left, 'peak_right': peak_right})
        else:
            return jsonify({'error': 'Failed to get audio levels'})
    except Exception as e:
        return jsonify({'error': f"Error: {e}"})
