import subprocess
import time

def connect_jack_ports():
    # Connect jack_capture input1 and input2 to system capture channels
    subprocess.run(['jack_connect', 'system:capture_1', 'jack_capture:input1'])
    subprocess.run(['jack_connect', 'system:capture_2', 'jack_capture:input2'])

def get_audio_levels():
    # Command to capture audio levels from jack_capture for input1 and input2 channels
    result = subprocess.run(['jack_capture', '-d', '1', '-c', '2', 'temp.wav'], capture_output=True, text=True)
    levels = parse_output(result.stdout)
    return levels

def parse_output(output):
    # Implement your logic to parse the output and extract audio levels
    # For example, parse the stdout for levels information and return a dictionary
    levels = {'input1': 0, 'input2': 0}  # Initialize levels
    # Parse output and update levels dictionary
    # Example logic for parsing (adjust according to actual output format):
    for line in output.split('\n'):
        if 'input1' in line:
            levels['input1'] = extract_level(line)
        elif 'input2' in line:
            levels['input2'] = extract_level(line)
    return levels

def extract_level(line):
    # Extract level from the line
    # Placeholder logic - update according to actual output format
    parts = line.split(':')
    if len(parts) > 1:
        try:
            return int(parts[1].strip())
        except ValueError:
            return 0
    return 0

def main():
    # Connect the jack ports
    connect_jack_ports()

    while True:
        levels = get_audio_levels()
        print(f"Input1 Level: {levels['input1']} | Input2 Level: {levels['input2']}")
        time.sleep(1)  # Adjust the sleep time as needed

if __name__ == "__main__":
    main()
