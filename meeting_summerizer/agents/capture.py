from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Generator

logger = logging.getLogger(__name__)


defensive_log = logger.debug


@dataclass
class CaptureConfig:
    meeting_id: str
    frame_count: int = 5


class CaptureAgent:
    """Simulates capturing audio frames from BigBlueButton."""

    def __init__(self, config: CaptureConfig) -> None:
        self.config = config
        defensive_log("CaptureAgent initialized with %s", self.config)

    def run(self) -> Generator[bytes, None, None]:
        """Yield dummy audio frames."""
        for i in range(self.config.frame_count):
            defensive_log("Capturing frame %d", i)
            yield f"audio_frame_{i}".encode()
        defensive_log("Capture complete")
