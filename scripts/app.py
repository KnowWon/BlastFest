from flask import Flask, render_template, jsonify
import subprocess
import time
import numpy as np
import wave

app = Flask(__name__)

def get_audio_levels(filename):
    try:
        # Convert the file to a standard PCM format using sox
        converted_filename = "converted_input.wav"
        subprocess.run(['sox', filename, '-b', '16', '-t', 'wav', converted_filename], check=True)
        
        # Read the converted WAV file
        with wave.open(converted_filename, 'rb') as wf:
            num_channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            frame_rate = wf.getframerate()
            num_frames = wf.getnframes()
            audio_data = wf.readframes(num_frames)

        # Convert audio data to numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        if audio_array.size == 0:
            raise ValueError("Empty audio array")

        # Compute peak levels for each channel
        peak_left = np.max(np.abs(audio_array[::2]))
        peak_right = np.max(np.abs(audio_array[1::2]))

        return peak_left, peak_right
    except Exception as e:
        print(f"Error: {e}")
        return None, None

@app.route('/audio_levels')
def audio_levels():
    try:
        print("Received request for audio levels")
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

if __name__ == "__main__":
    app.run(debug=True)
