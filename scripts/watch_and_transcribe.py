# The script below is the first version of this pipeline - with transcription record creation in SQLite. The current version does not include keyword metadata and generates transcription records in PostgreSQL.

import os
import sqlite3
import subprocess
import re
from datetime import datetime

#-------------------Configuration-------------------
RAW_AUDIO_DIR = os.path.expanduser("~/Whispersync/whispersync_panel/raw_audio")
TRANSCRIPT_DIR = os.path.expanduser("~/Whispersync/whispersync_panel/transcripts")
DB_PATH = os.path.expanduser("~/Whispersync/whispersync_panel/whispersync.db")
CLEAN_SCRIPT = os.path.expanduser("~/Whispersync/whispersync_panel/scripts/clean-filenames.sh")
DIRTY_AUDIO = os.path.expanduser("~/Whispersync/whispersync_panel/dirty_audio")
LOG_SCRIPT = os.path.expanduser("~/Whispersync/whispersync_panel/scripts/whisper_transcript_log.sh")
TAG_KEYWORDS = [
    "madness", "writing", "death", "music", "loss", "chapter", "prologue", "epilogue", "theme", "dream", "voice", "echo", "colombia", "adoption", "love", "gift", "abuse"]

#-------------------Setup Directories-------------------
os.makedirs(RAW_AUDIO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(DIRTY_AUDIO, exist_ok=True)

def process_all_files():
    #-------------------Batch Cleaning Step-------------------
    result = subprocess.run([CLEAN_SCRIPT, DIRTY_AUDIO])
    if result.returncode != 0:
        print(f"[!] Error cleaning files in {DIRTY_AUDIO}")
    else:
        print(f"Using clean script at: {CLEAN_SCRIPT}")

#-------------------Process Audio Files-------------------

    files_processed = 0
    for fname in os.listdir(RAW_AUDIO_DIR):
        fpath = os.path.join(RAW_AUDIO_DIR, fname)
        base_name, ext = os.path.splitext(fname)
        transcript_path = os.path.join(TRANSCRIPT_DIR, base_name + ".txt")
        if (
            fname.lower().endswith(".m4a")
            and os.path.isfile(fpath)
            and not os.path.exists(transcript_path)  # <--- only if not already transcribed
        ):
            print(f"[Processing] Found audio file: {fpath}")
            process_audio(fpath)
            files_processed += 1
        elif fname.lower().endswith(".m4a") and os.path.exists(transcript_path):
            print(f"[SKIP] Transcript already exists for {fpath}, skipping.")
    if files_processed == 0:
        print("No audio files to process in raw_audio.")

def process_audio(audio_path):
    filename = os.path.basename(audio_path)
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(TRANSCRIPT_DIR, f"{base_name}.txt")

    print(f"[~] Transcribing {filename} to {output_path}")
    result = subprocess.run(
        [
            "whisper", audio_path, "--output_dir", TRANSCRIPT_DIR,
            "--model", "base", "--language", "en"
        ],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"[!] Whisper transcription failed for {filename}: {result.stderr}")
        return

    transcript_file = output_path
    if not os.path.exists(transcript_file):
        print(f"[!] Transcript file not found after transcription: {transcript_file}")
        return

#-------------------Extract Metadata and Tags-------------------

    with open(transcript_file, 'r', encoding='utf-8') as f:
        content = f.read()

    word_count = len(content.split())
    tags = []
    content_lower = content.lower()
    for tag in TAG_KEYWORDS:
        if re.search(r'\b' + re.escape(tag.lower()) + r'\b', content_lower):
            tags.append(tag)

    # ---------------------LOGGING --------------------------------
    STAMP = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    FILENAME = filename
    subprocess.run([LOG_SCRIPT, "SUCCESS", STAMP, FILENAME])
    print(f"Creating log entry for {FILENAME} at {STAMP}")

#----------------------Store metadata in SQLite database--------------------
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT,
            filename TEXT,
            filepath TEXT,
            word_count INTEGER,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        INSERT INTO sources (source_type, filename, filepath, word_count, tags)
        VALUES (?, ?, ?, ?, ?)
    ''', ("transcript", filename, transcript_file, word_count, ','.join(tags)))
    conn.commit()
    conn.close()

    print(f"[+] Transcription complete and saved: {transcript_file}")
    print(f"[+] Metadata written to db with tags: {tags}")
    print("Your new database entry awaits your inspection!")

#-------------------Repair DB for Missing Transcripts-------------------
def repair_db_for_transcripts():
    print("\n Repairing database for missing transcript records...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT,
            filename TEXT,
            filepath TEXT,
            word_count INTEGER,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
    ''')
    # Get all transcript records in DB
    cursor.execute("SELECT filename FROM sources WHERE source_type='transcript'")
    existing = set(row[0] for row in cursor.fetchall())
    # Find all .txt files in the transcript directory
    files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith('.txt')]
    inserted = 0

    for f in files:
        if f in existing:
            print(f"✔ DB record exists for {f}")
            continue

        transcript_path = os.path.join(TRANSCRIPT_DIR, f)
        with open(transcript_path, 'r', encoding='utf-8') as txtfile:
            content = txtfile.read()
        word_count = len(content.split())
        tags = []
        content_lower = content.lower()
        for tag in TAG_KEYWORDS:
            if re.search(r'\b' + re.escape(tag.lower()) + r'\b', content_lower):
                tags.append(tag)
        
        cursor.execute('''
            INSERT INTO sources (source_type, filename, filepath, word_count, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', ("transcript", f, transcript_path, word_count, ','.join(tags)))
        conn.commit()
        inserted += 1
        print(f"➕ Added missing DB record for {f} with tags: {tags}")
    
    conn.close()
    print(f" [✔] Repair complete. {inserted} new records added to the database.\n")


#-------------------Main Script-------------------
if __name__ == "__main__":
    while True:
        process_all_files()
        answer = input("\nWould you like to process another file? (y/n): ").strip().lower()
        if answer != 'y':
            print("See ya next time! Goodbye!")
            break
        print("\nAdd your next file to 'dirty_audio' and press Enter when ready.")
        input()
