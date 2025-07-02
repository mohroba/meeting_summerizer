# Meeting Summarizer

This project provides a modular pipeline to capture audio from BigBlueButton (BBB) sessions,
transcribe them in real time via a Whisper Live server, store the captions in Postgres,
chunk them, and summarize using an LLM.
The pipeline is orchestrated with Prefect.

## Requirements

- Python 3.12+
- Docker (for running via `docker-compose`)

## Usage

### Local

```bash
pip install -r requirements.txt
python -m meeting_summerizer.main
```

### Docker Compose

```bash
docker-compose up --build
```

Docker Compose starts Postgres, Whisper Live, Ollama, and the Prefect-based pipeline.

Environment variables:

- `BBB_URL` – base URL of your BBB server
- `BBB_SECRET` – shared secret for API access
- `MEETING_ID` – meeting identifier to capture
- `DB_URL` – SQLAlchemy database URL
- `WHISPER_URL` – WebSocket URL of Whisper Live server
- `OLLAMA_HOST` – base URL of the Ollama server (optional)
- `OLLAMA_MODEL` – model name to use for summarization

The application will log generated summaries.
