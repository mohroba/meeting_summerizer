from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, Generator

logger = logging.getLogger(__name__)

defensive_log = logger.debug


@dataclass
class ChunkingConfig:
    size: int = 3


class ChunkingAgent:
    """Chunks transcripts into fixed-size batches."""

    def __init__(self, config: ChunkingConfig) -> None:
        self.config = config
        defensive_log("ChunkingAgent initialized with %s", self.config)

    def run(self, transcripts: Iterable[str]) -> Generator[list[str], None, None]:
        chunk: list[str] = []
        for text in transcripts:
            chunk.append(text)
            if len(chunk) >= self.config.size:
                defensive_log("Yielding chunk: %s", chunk)
                yield chunk
                chunk = []
        if chunk:
            defensive_log("Yielding final chunk: %s", chunk)
            yield chunk
        defensive_log("Chunking complete")
