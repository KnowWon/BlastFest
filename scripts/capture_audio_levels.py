import subprocess
import time

def get_audio_levels():
    try:
        # Get the volume levels of the capture devices
        result = subprocess.run(['amixer', 'sget', 'Capture'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    try:
        print("Monitoring audio levels. Press Ctrl+C to stop.")
        while True:
            # Get and print the audio levels
            levels = get_audio_levels()
            if levels:
                print(levels)
            time.sleep(1)  # Update every second
    except KeyboardInterrupt:
        print("Stopping audio level monitoring.")

if __name__ == "__main__":
    main()
