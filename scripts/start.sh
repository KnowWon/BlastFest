#!/bin/bash

# Path to your scripts
start_jack="/var/www/blast.beat/scripts/start_jack.sh"
# capture_levels="/var/www/blast.beat/scripts/capture_levels.sh"
app="/var/www/blast.beat/scripts/app.py"
capture_audio_levels="/var/www/blast.beat/scripts/capture_audio_levels.py"

# Log directory
log_dir="/var/www/blast.beat/logs"

# Log files to be purged
log_files=("app.log" "capture_audio_levels.log")

# Purge existing log files
echo "Purging existing log files..."
for file in "${log_files[@]}"; do
    rm -f "$log_dir/$file"
done

# Run the scripts
echo "Starting JACK server..."
$start_jack
echo "JACK server started."

# Wait for the jackd to start
sleep 5

echo "Running Capture Audio Levels Python Script"
python3 $capture_audio_levels >> $log_dir/capture_audio_levels.log 2>&1 &
echo "Capture Audio Levels Python script running in the background."

# Wait for the audio capture to start
sleep 5

# Stop existing instances of app.py
echo "Stopping existing instances of app.py..."
sudo pkill -f "python3 $app"
# Ensure log directory exists
mkdir -p $log_dir

echo "Running App Python script..."
python3 $app >> $log_dir/app.log 2>&1 &
echo "App Python script running in the background."




