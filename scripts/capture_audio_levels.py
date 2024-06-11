import subprocess
import requests
import time

def connect_jack_ports():
    subprocess.run(['jack_connect', 'system:capture_1', 'jack_capture:input1'])
    subprocess.run(['jack_connect', 'system:capture_2', 'jack_capture:input2'])

def get_audio_levels():
    try:
        result = subprocess.run(['jack_capture', '-d', '1', '-c', '2', 'input2.wav'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error capturing audio: {result.stderr}")
            return {'input1': 0, 'input2': 0}
        levels = parse_output(result.stdout)
        return levels
    except Exception as e:
        print(f"Exception during audio capture: {e}")
        return {'input1': 0, 'input2': 0}

def parse_output(output):
    levels = {'input1': 0, 'input2': 0}
    for line in output.split('\n'):
        if 'input1' in line:
            levels['input1'] = extract_level(line)
        elif 'input2' in line:
            levels['input2'] = extract_level(line)
    return levels

def extract_level(line):
    parts = line.split(':')
    if len(parts) > 1:
        try:
            return int(parts[1].strip())
        except ValueError:
            return 0
    return 0

def send_levels_to_server(levels):
    url = 'http://127.0.0.1:5000/upload_levels'
    data = {'input1': levels['input1'], 'input2': levels['input2']}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error sending levels to server: {e}")
        return None

connect_jack_ports()

while True:
    levels = get_audio_levels()
    print(f"Captured levels: {levels}")
    status = send_levels_to_server(levels)
    if status == 200:
        print("Successfully sent levels to server")
    else:
        print("Failed to send levels to server")
    time.sleep(1)
