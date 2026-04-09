#!/bin/bash
# transcribe.sh - Bulk transcribe all audio files in a given folder
# use this for on-demand transcription

AUDIO_DIR="$1"

if [ ! -d "$AUDIO_DIR" ]; then
    echo "❌ Directory not found: $AUDIO_DIR"
    exit 1
fi

for audio_file in "$AUDIO_DIR"/*.m4a; do
    ./whisper-transcribe.sh "$audio_file"
done

