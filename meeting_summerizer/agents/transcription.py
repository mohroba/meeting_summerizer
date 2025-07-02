from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Generator, Iterable

logger = logging.getLogger(__name__)

defensive_log = logger.debug


@dataclass
class TranscriptionConfig:
    language: str = "en"


class TranscriptionAgent:
    """Dummy transcription converting audio frames to text."""

    def __init__(self, config: TranscriptionConfig) -> None:
        self.config = config
        defensive_log("TranscriptionAgent initialized with %s", self.config)

    def run(self, frames: Iterable[bytes]) -> Generator[str, None, None]:
        for i, frame in enumerate(frames):
            defensive_log("Transcribing frame %d: %s", i, frame)
            yield f"transcript {i} for {self.config.language}"
        defensive_log("Transcription complete")
