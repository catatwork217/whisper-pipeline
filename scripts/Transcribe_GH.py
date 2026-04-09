# This is the current version of this pipeline. DB transcription records get generated through PostgreSQL.

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import psycopg2
import os
from datetime import datetime
import whisper
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transcribe_and_store(audio_path: str) -> None:
    try:
        logger.info(f"Processing {audio_path}...")
        model = whisper.load_model("base")
        logger.info("Model loaded successfully.")
        result = model.transcribe(audio_path)
        text = result["text"]
        word_count = len(text.split())
        file_size = os.path.getsize(audio_path)
        original_filename = os.path.basename(audio_path)
        created_at = updated_at = datetime.now()

        # Save transcription as a text file
        base_filename = os.path.splitext(original_filename)[0]
        output_dir = "path_to_output_file"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{base_filename}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Transcription saved to: {output_file}")

        # Store in PostgreSQL
        with psycopg2.connect(
            dbname="YOURDBNAME",
            user="YOURUSERNAME",
            password="DBPW",
            host="localhost"
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO book.transcriptions_book
                    (original_filename, file_size, word_count, transcription_text, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (original_filename, file_size, word_count, text, created_at, updated_at)
                )
                logger.info(f"Database record inserted for: {original_filename}")

    except psycopg2.IntegrityError:
        logger.error(f"Duplicate filename detected: {original_filename}")
    except psycopg2.Error as db_error:
        logger.error(f"Database error for {audio_path}: {db_error}")
    except Exception as e:
        logger.error(f"Error processing {audio_path}: {e}", exc_info=True)

def process_audio_files(directory: str) -> None:
    if not os.path.exists(directory):
        logger.error(f"Directory not found: {directory}")
        return

    logger.info(f"Processing directory: {directory}")
    supported_extensions = [".m4a"]  # Only process .m4a files
    audio_files = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in supported_extensions]
    logger.info(f"Found {len(audio_files)} audio files to process.")

    for filename in audio_files:
        audio_path = os.path.join(directory, filename)
        transcribe_and_store(audio_path)

if __name__ == "__main__":
    audio_directory = "Directory_where_all_audio_new_audio_stored"
    process_audio_files(audio_directory)
    logger.info("Transcription process completed.")
