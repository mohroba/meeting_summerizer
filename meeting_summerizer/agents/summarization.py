from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, List

import ollama

logger = logging.getLogger(__name__)

defensive_log = logger.debug


@dataclass
class SummarizationConfig:
    model: str = "llama2"
    host: str | None = None


class SummarizationAgent:
    """Produces a naive summary from transcript chunks."""

    def __init__(self, config: SummarizationConfig) -> None:
        self.config = config
        self.client = ollama.Client(host=self.config.host) if self.config.host else ollama
        defensive_log("SummarizationAgent initialized with %s", self.config)

    def run(self, chunks: Iterable[List[str]]) -> List[str]:
        summaries: List[str] = []
        for chunk in chunks:
            text = " ".join(chunk)
            defensive_log("Summarizing chunk: %s", text)
            resp = self.client.chat(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Summarize key points, decisions, and action items.",
                    },
                    {"role": "user", "content": text},
                ],
            )
            summaries.append(resp.message.content.strip())
        defensive_log("Summarization complete")
        return summaries
