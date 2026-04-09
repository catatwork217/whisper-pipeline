#!/bin/bash

# Use this script as a stand-alone script to clean filenames prior to running a bulk-transcribe function - or incorporate this into a transription script like the 'watch_and_transcribe.py' or 'Transcribe_GH.py' script.

INPUT="$1"
echo "🎧 Cleaning filenames for CLI safety..."

if [ ! -e "$INPUT" ]; then
    echo "❌ Error: Path does not exist: $INPUT"
    exit 1
fi

# Handle a single file
if [ -f "$INPUT" ]; then
    DIR=$(dirname "$INPUT")
    FILE=$(basename "$INPUT")
    CLEANED=$(echo "$FILE" | tr ' ' '_' | tr -d '"\'\!')

    if [ "$FILE" != "$CLEANED" ]; then
        mv "$DIR/$FILE" "$DIR/$CLEANED"
        echo "✅ Renamed: $FILE → $CLEANED"
    else
        echo "ℹ️ No cleanup needed: $FILE"
    fi

# Handle a folder
elif [ -d "$INPUT" ]; then
    cd "$INPUT" || exit 1
    for FILE in *; do
	CLEANED=$(echo "$FILE" | tr ' ' '_' | tr -d '"!'\''\\')
	if [ "$FILE" != "$CLEANED" ]; then
            mv "$FILE" "$CLEANED"
            echo "✅ Renamed: $FILE → $CLEANED"
        fi
    done
else
    echo "❌ Not a valid file or directory."
    exit 1
fi

