# Meeting Summarizer

This project provides a modular pipeline to capture audio from BigBlueButton sessions,
transcribe it using a dummy ASR, store transcripts, chunk them, and produce simple summaries.
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

The application will log generated summaries.
