import subprocess
import time

def start_jack_meter():
    # Start jack_meter in the background
    process = subprocess.Popen(['jack_meter', 'system:capture_1', 'system:capture_2'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def read_levels(process):
    while True:
        line = process.stdout.readline()
        if line:
            print(line.strip())
        time.sleep(0.1)  # Adjust the sleep time as needed

def main():
    # Start the jack_meter process
    process = start_jack_meter()
    
    try:
        # Read and print levels from the jack_meter process
        read_levels(process)
    except KeyboardInterrupt:
        print("Stopping audio level monitoring.")
        process.terminate()

if __name__ == "__main__":
    main()

