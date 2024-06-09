import subprocess
import time

def start_jack_metro():
    # Start jack_metro in the background for two channels
    process = subprocess.Popen(['jack_metro', '-m', 'vu', 'system:capture_1', 'system:capture_2'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def main():
    # Start the jack_metro process
    process = start_jack_metro()
    
    try:
        print("Jack Metro started. Press Ctrl+C to stop.")
        while True:
            # Read and print output to keep the process running and check for any errors
            output = process.stdout.readline().strip()
            if output:
                print(output)
            time.sleep(1)  # Keep the script running to maintain the jack_metro process
    except KeyboardInterrupt:
        print("Stopping audio level monitoring.")
        process.terminate()

if __name__ == "__main__":
    main()
