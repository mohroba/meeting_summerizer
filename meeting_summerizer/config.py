from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    db_url: str
    meeting_id: str
    bbb_url: str
    bbb_secret: str
    whisper_url: str
    ollama_host: str | None
    ollama_model: str


def get_settings() -> Settings:
    return Settings(
        db_url=os.getenv("DB_URL", "sqlite:///data.db"),
        meeting_id=os.getenv("MEETING_ID", "demo-meeting"),
        bbb_url=os.getenv("BBB_URL", "http://localhost:7001"),
        bbb_secret=os.getenv("BBB_SECRET", "secret"),
        whisper_url=os.getenv("WHISPER_URL", "ws://localhost:9000/ws"),
        ollama_host=os.getenv("OLLAMA_HOST"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama2"),
    )
