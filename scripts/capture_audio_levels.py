import subprocess
import time
import numpy as np

def get_audio_levels():
    try:
        # Record a short snippet of audio
        process = subprocess.run(
            ['arecord', '-D', 'plughw:0,0', '-f', 'cd', '-t', 'raw', '-d', '1'],
            capture_output=True
        )
        audio_data = process.stdout

        # Convert audio data to numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        # Compute peak levels
        peak_left = np.max(np.abs(audio_array[::2]))
        peak_right = np.max(np.abs(audio_array[1::2]))

        return peak_left, peak_right
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def main():
    try:
        print("Monitoring audio levels. Press Ctrl+C to stop.")
        while True:
            peak_left, peak_right = get_audio_levels()
            if peak_left is not None and peak_right is not None:
                print(f"Peak Left: {peak_left}, Peak Right: {peak_right}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping audio level monitoring.")

if __name__ == "__main__":
    main()
