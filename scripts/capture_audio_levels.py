import subprocess
import time

def start_meterbridge():
    # Start meterbridge in the background for two channels
    process = subprocess.Popen(['meterbridge', '-t', 'vu', 'system:capture_1', 'system:capture_2'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def main():
    # Start the meterbridge process
    process = start_meterbridge()
    
    try:
        print("Meterbridge started. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)  # Keep the script running to maintain the meterbridge process
    except KeyboardInterrupt:
        print("Stopping audio level monitoring.")
        process.terminate()

if __name__ == "__main__":
    main()
