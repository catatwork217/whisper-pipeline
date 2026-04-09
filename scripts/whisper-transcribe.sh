# The shell script below is the initial stand-alone transcription script - designed to remain an 'on-demand' script that a User may run in terminal or at the command line.

#!/bin/bash

AUDIO_FILE="$1"
MODEL="medium"
OUTDIR="$HOME/Whispersync/transcripts"
LOGFILE="$HOME/Whispersync/transcript-log.txt"

if [ ! -f "$AUDIO_FILE" ]; then
	echo "Audio file not found: $AUDIO_FILE"
	exit 1
fi

mkdir -p "$OUTDIR"

# Transcribe
/home/anaconda3/bin/whisper "$AUDIO_FILE" \
	--model "$MODEL" \
	--language English \
	--output_dir "$OUTDIR" \
	--output_format txt \
	--verbose False
	
# Added to incorporate whisper_transcript_log.sh into this script for 1-step file and log


# Log it
STAMP=$(date '+%Y-%m-%d %H:%M:%S')
FILENAME=$(basename "$AUDIO_FILE")
echo "[$STAMP] Transcribed: $FILENAME → $OUTDIR/${FILENAME%.*}.txt" >> "$LOGFILE"

echo "Transcript saved + logged."


