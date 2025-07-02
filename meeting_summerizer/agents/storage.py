from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable

from datetime import datetime
from sqlalchemy import (Column, DateTime, Integer, String, UniqueConstraint,
                        create_engine)
from sqlalchemy.orm import declarative_base, Session

logger = logging.getLogger(__name__)

defensive_log = logger.debug

Base = declarative_base()


class Caption(Base):
    __tablename__ = "captions"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, nullable=False, index=True)
    ts = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("session_id", "ts", "text", name="uniq_cap"),)


@dataclass
class StorageConfig:
    db_url: str = "sqlite:///data.db"
    session_id: str = "default"


class StorageAgent:
    """Stores transcripts in a database."""

    def __init__(self, config: StorageConfig) -> None:
        self.config = config
        self.engine = create_engine(self.config.db_url)
        Base.metadata.create_all(self.engine)
        defensive_log("StorageAgent initialized with %s", self.config)

    def run(self, captions: Iterable[dict]) -> None:
        with Session(self.engine) as session:
            for caption in captions:
                defensive_log("Storing caption: %s", caption)
                obj = Caption(
                    session_id=self.config.session_id,
                    ts=int(caption.get("timestamp", 0)),
                    text=caption.get("text", ""),
                )
                try:
                    session.add(obj)
                    session.commit()
                except Exception:
                    session.rollback()
        defensive_log("Storage complete")
        # dispose connection to ensure SQLite writes to disk
        self.engine.dispose()

    def fetch_all(self) -> list[str]:
        with Session(self.engine) as session:
            rows = session.query(Caption).filter_by(session_id=self.config.session_id).all()
            return [row.text for row in rows]
