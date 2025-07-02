from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Generator, Iterable

import json
from websockets.sync.client import connect

logger = logging.getLogger(__name__)

defensive_log = logger.debug


@dataclass
class TranscriptionConfig:
    ws_url: str = "ws://localhost:9000/ws"
    language: str = "en"


class TranscriptionAgent:
    """Stream audio frames to Whisper Live and yield transcripts."""

    def __init__(self, config: TranscriptionConfig) -> None:
        self.config = config
        defensive_log("TranscriptionAgent initialized with %s", self.config)

    def run(self, frames: Iterable[bytes]) -> Generator[dict, None, None]:
        with connect(self.config.ws_url, max_size=2 ** 20) as ws:
            for i, frame in enumerate(frames):
                defensive_log("Sending frame %d", i)
                ws.send(frame)
                resp = ws.recv()
                try:
                    data = json.loads(resp)
                    yield {
                        "timestamp": data.get("timestamp", i),
                        "text": data.get("text", ""),
                    }
                except json.JSONDecodeError:
                    defensive_log("Invalid response: %s", resp)
        defensive_log("Transcription complete")
