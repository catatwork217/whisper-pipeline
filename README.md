
# 🎤 Automated Transcription Pipeline
**Empowering Users with Open-Source, Low-Code Transcription and Metadata Management**

---

## 📌 Description
An open-source, low-code automated transcription pipeline designed to produce speech-to-text files with metadata indexing and data management capabilities. This pipeline bridges the gap between analog and digital formats, enabling users to transcribe, index, and analyze audio files efficiently.

---

[Integrated PostgreSQL & PgAdmin for enhanced dB integration and management capability.]: #

## 🔧 Tools and Technologies
- **PostgreSQL**: Database management for storing and querying transcription metadata.
- **pgAdmin**: GUI for database administration and visualization.
- **Python**: Scripting for automation, transcription, and data processing.
- **Docker**: Containerization for easy deployment and accessibility.

---

## 📂 Script Overview

| Script                          | Description                                                                                         |
|----------------------------------|-----------------------------------------------------------------------------------------------------|
| `whisper-transcribe.sh`          | Transcribes a single audio file using Whisper CLI (pipeline v1; standalone or building block)        |
| `clean-filenames.sh`             | Cleans audio file names for safety (pipeline v1–v2; standalone or utility)                          |
| `whisper_transcript_log.sh`      | Logs transcription events with status, timestamp, and filename for auditability                     |
| `watch_and_transcribe.py`        | This is the first version of this pipeline with keyword metadata, word count, and db record creation in SQLite:
      Cleans filenames, batch transcribes, extracts keywords, counts word length, logs, stores in **SQLite**, includes built-in DB repair utility |
| `repair_transcript_db.py`        | **Standalone** on-demand utility to repair or rebuild your transcript DB from existing transcript files (for bulk recovery, troubleshooting, or advanced workflows) |
| `Transcribe_GH.py`                  | **Updated for use with postgreSQL & PgAdmin** Python script that enables User to save output to **PostgreSQL** dB that may be managed via CLI or **PgAdmin** GUI. |

> **Note:** The original bash scripts (`whisper-transcribe.sh`, `clean-filenames.sh`, `whisper_transcript_log.sh`) represent earlier iterations of this pipeline and are preserved for reference, reproducibility, and modular use.
> **Earlier version full pipeline:** `watch_and_transcribe.py` & `repair_transcript_db.py`
> **Current iteration:** `Transcribe_GH.py` for use with postgreSQL, pgAdmin, and duplicate check.

---

## 🚀 Features
- **Automated Transcription**: Uses Whisper and Python to convert audio files into timestamped text.
- **Metadata Indexing**: Stores transcription data in a **PostgreSQL** database, including file size, original filename, word count, keywords, and incorporation status.
- **Query Capability**: Enables users to search, filter, and analyze transcriptions using SQL queries.
- **Data Visualization**: Generates graphs and visualizations (e.g., word count tracking) directly from the database.
- **User-Friendly**: Docker container and GUI in development for non-technical users.

---

## 📊 Database Schema
The PostgreSQL database includes the following columns for each transcription record:
- 'id'
- 'original_filename'
- 'file_size'
- 'word_count'
- 'transcription_text'
- 'created_at'
- 'updated_at'


Example query to retrieve transcriptions:
```sql
SELECT * FROM memoir_recordings ORDER BY word_count DESC;
```

---

## 🖼️ Project Evolution
**Updated**
- Pipeline - Overview and value proposition, viewable at [cathrinmcdougall.com/transcription-pipeline](https://www.cathrinmcdougall.com/transcription-pipeline)

---

## 📁 Examples
Included in the [Examples/](Examples/) are sample files to show what the outputs will look like in all formats: `.txt`, `.tsv`, `.vtt`, `.srt`, `json`.
- **JSON**: For integration with REST APIs.
- **SRT/VTT**: Different accessibility captions file formats.
- **TXT**: Regular text file format for import or conversion to any word processing format needed.
- **TSV**: Organizes the transcript into a tabular format for easy editing and continued work in spreadsheet or as a database export.

---

## 🚧 TODO / In Progress
- Docker containerization

---

## ❗ Current Limitations
- Backend only

---

## 💬 Future Goals
- Docker containerization
- GUI for non-technical User access
- Agentic workflow
---

## 🤝 License
Licensed under the GNU General Public License v2.0. See [LICENSE](LICENSE).

---

## 👩‍💻 Author
**Cathrin McDougall**
Certified Scrum Master & Product Owner
**Passionate advocate of AI Governance & ethical application of AI**
[Substack-AgileEveryday](https://substack.com/@agileeveryday) | [GitHub](https://github.com/catatwork217)
