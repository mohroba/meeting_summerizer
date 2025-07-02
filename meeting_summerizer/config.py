from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    db_url: str
    meeting_id: str


def get_settings() -> Settings:
    return Settings(
        db_url=os.getenv("DB_URL", "sqlite:///data.db"),
        meeting_id=os.getenv("MEETING_ID", "demo-meeting"),
    )
