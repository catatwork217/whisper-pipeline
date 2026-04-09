# This script may be run against an existing db with transcribed records - to check for duplicates against existing db.

import os
import sqlite3
import re
from datetime import datetime

# ---- Config - update if needed ----
TRANSCRIPT_DIR = os.path.expanduser("~/Whispersync/whispersync_panel/transcripts")
DB_PATH = os.path.expanduser("~/Whispersync/whispersync_panel/whispersync.db")
TAG_KEYWORDS = [
    "madness", "writing", "death", "music", "loss", "chapter", "prologue", "epilogue",
    "theme", "dream", "voice", "echo"]

def get_existing_filenames(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM sources WHERE source_type='transcript'")
    return set(row[0] for row in cursor.fetchall())

def extract_tags(text):
    tags = []
    content_lower = text.lower()
    for tag in TAG_KEYWORDS:
        if re.search(r'\b' + re.escape(tag.lower()) + r'\b', content_lower):
            tags.append(tag)
    return tags

def main():
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
    existing = get_existing_filenames(conn)
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
        tags = extract_tags(content)

        # Insert into DB
        cursor.execute('''
            INSERT INTO sources (source_type, filename, filepath, word_count, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', ("transcript", f, transcript_path, word_count, ','.join(tags)))
        conn.commit()
        inserted += 1
        print(f"➕ Added missing DB record for {f} with tags: {tags}")

    conn.close()
    print(f"All done! {inserted} record(s) added. {len(files) - inserted} already present.")

if __name__ == "__main__":
    main()
