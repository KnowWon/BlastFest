# BlastFest

Purpose of this project is to detect when a BlastBeat is being played on a drun kit and calculate the speed.
Then display on a webpage when a BlastBeat is being played and what BPM it is being played at.

Physical equipment:
Raspberry Pi with Debian no GUI which is hosting webpage, SQL, attached to audio interface, running programs to calculate BlastBeat
Audio Interface Presonus AudioBox 44VSL, connected to above Raspberry Pi
2x Clip-On Contact Microphones, connected to Audio Interface

Raspberry Pi, with GUI, running in Kiosk mode, outputting webage from above set up, connected to display

Xiaomi Tablet, used to administer and configure the 2 machines above. Also with Festivals will be able to calibrate Microphone levels, Change page displayed on kiosk pi to one showing highscores for in between bands, change the band playing

WiFi router, to connect all the systems

Method:
I'm using ChatGPT to help me code this.
Stage 1:
There is 1 Mic on the Kick Drum and 1 on the Snare drum, these are going into Input 1 and 2 respectively on the Audio Interface
A program configures Jackd and Alsa at start up so that these Inputs are connected to Left and Right Outputs, This part is currently working.
Stage 2:
Get a program to detect when a level has been detected on each microphone
Stage 3:
Next I want to show the Outputs on a webpage where a trigger level can be set, this will be the calibration page and mean that the trigger levels can be dynamically adjusted without having to manually adjust the levels on the audio interface.
Stage 4:
Next I will look for a pattern where the trigger level is hit alternating between the 2 mics, with a constant-ish frequency. So will look for a consistent tempo matched on both inputs.
When it detects this (4 hits on each mic could be the trigger to show that blastbeat is being played) 
Stage 5:
Calculate the speed in BPM assuming 8th notes played on each input
Stage 6:
Display on a webpage when a blastbeat has been detected and it's speed
Stage 7:
Remember the fastest blastbeat in a table
Stage 8:
Multiple bands, which can be switched between by controller tablet.
Stage 9: 
High scores displayed inbetween bands

Programs run:
/scripts/start.sh in Cronjob at reboot

