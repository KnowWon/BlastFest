#!/bin/bash

# Function to find the card number for "AudioBox 44 VSL"
find_card_number() {
  aplay -l | grep -A 1 "AudioBox 44 VSL" | grep -oP 'card \K[0-9]+'
}

# Get the card number for AudioBox 44 VSL
CARD_NUMBER=$(find_card_number)

if [ -z "$CARD_NUMBER" ]; then
  echo "Error: AudioBox 44 VSL not found."
  exit 1
fi

# Stop any existing JACK server
killall -9 jackd

# Start JACK server with the correct card number
export JACK_NO_AUDIO_RESERVATION=1
jackd -r -d alsa -d hw:$CARD_NUMBER -r 48000 -p 256 -n 3 &

# Wait for JACK server to start
sleep 5

# Connect the capture and playback ports
jack_connect system:capture_1 system:playback_1
jack_connect system:capture_2 system:playback_2

echo "JACK server started and connections established." >> ~/start_jack.log 2>&1
