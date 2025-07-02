from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Generator, Iterable

import requests

logger = logging.getLogger(__name__)


defensive_log = logger.debug


@dataclass
class CaptureConfig:
    bbb_url: str
    secret: str
    meeting_id: str
    frame_count: int = 5


class BBBClient:
    """Minimal BigBlueButton API client for audio streaming."""

    def __init__(self, url: str, secret: str) -> None:
        self.url = url.rstrip("/")
        self.secret = secret
        defensive_log("BBBClient initialized for %s", self.url)

    def join_audio(self, meeting_id: str) -> Iterable[bytes]:
        """Yield PCM audio frames from BBB."""
        params = {"meetingID": meeting_id, "secret": self.secret}
        resp = requests.get(f"{self.url}/api/audio", params=params, stream=True, timeout=10)
        resp.raise_for_status()
        for chunk in resp.iter_content(chunk_size=4096):
            if chunk:
                yield chunk


class CaptureAgent:
    """Capture audio frames from BigBlueButton."""

    def __init__(self, config: CaptureConfig) -> None:
        self.config = config
        self.client = BBBClient(config.bbb_url, config.secret)
        defensive_log("CaptureAgent initialized with %s", self.config)

    def run(self) -> Generator[bytes, None, None]:
        """Yield audio frames from BBB."""
        stream = self.client.join_audio(self.config.meeting_id)
        for i, frame in enumerate(stream):
            defensive_log("Capturing frame %d", i)
            yield frame
            if i + 1 >= self.config.frame_count:
                break
        defensive_log("Capture complete")
