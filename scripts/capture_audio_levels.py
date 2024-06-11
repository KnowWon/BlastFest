import requests
import time
import subprocess
import numpy as np
import wave
import os

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
    finally:
        # Clean up temporary files
        if os.path.exists(converted_filename):
            os.remove(converted_filename)

def capture_audio():
    while True:
        try:
            # Capture audio using jack_capture
            subprocess.run(['jack_capture', '-d', '1', '-c', '2', 'input2.wav'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Get audio levels from the captured file
            peak_left, peak_right = get_audio_levels('input2.wav')
            if peak_left is not None and peak_right is not None:
                levels = {'input1': int(peak_left), 'input2': int(peak_right)}
                print(f"Captured levels: {levels}")
                response = requests.post('http://127.0.0.1:5000/upload_levels', json=levels)
                response.raise_for_status()
                print("Successfully sent levels to server")
            else:
                print("Failed to get valid audio levels")
        except Exception as e:
            print(f"Error capturing audio or sending levels: {e}")
        finally:
            if os.path.exists('input2.wav'):
                os.remove('input2.wav')

        time.sleep(1)

if __name__ == "__main__":
    capture_audio()
