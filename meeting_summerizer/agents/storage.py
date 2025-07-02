from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, Optional

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

defensive_log = logger.debug

Base = declarative_base()


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)


@dataclass
class StorageConfig:
    db_url: str = "sqlite:///data.db"


class StorageAgent:
    """Stores transcripts in a database."""

    def __init__(self, config: StorageConfig) -> None:
        self.config = config
        self.engine = create_engine(self.config.db_url)
        Base.metadata.create_all(self.engine)
        defensive_log("StorageAgent initialized with %s", self.config)

    def run(self, transcripts: Iterable[str]) -> None:
        with Session(self.engine) as session:
            for text in transcripts:
                defensive_log("Storing transcript: %s", text)
                session.add(Transcript(text=text))
            session.commit()
        defensive_log("Storage complete")
        # dispose connection to ensure SQLite writes to disk
        self.engine.dispose()

    def fetch_all(self) -> list[str]:
        with Session(self.engine) as session:
            rows = session.query(Transcript).all()
            return [row.text for row in rows]
