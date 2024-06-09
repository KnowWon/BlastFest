import subprocess
import time
import numpy as np
import wave

def get_audio_levels(filename):
    try:
        # Convert the file to a standard PCM format using sox
        converted_filename = "converted_input.wav"
        subprocess.run(['sox', filename, '-b', '16', converted_filename], check=True)
        
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

def main():
    try:
        print("Monitoring audio levels. Press Ctrl+C to stop.")
        while True:
            # Capture audio using jack_capture
            subprocess.run(['jack_capture', '-d', '1', '-c', '2', 'input2.wav'])

            # Get audio levels from the captured file
            peak_left, peak_right = get_audio_levels('input2.wav')
            if peak_left is not None and peak_right is not None:
                print(f"Peak Left: {peak_left}, Peak Right: {peak_right}")

            # Sleep for a second before the next capture
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping audio level monitoring.")

if __name__ == "__main__":
    main()
