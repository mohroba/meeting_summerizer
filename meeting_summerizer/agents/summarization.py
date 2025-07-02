from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, List

logger = logging.getLogger(__name__)

defensive_log = logger.debug


@dataclass
class SummarizationConfig:
    sentence_count: int = 2


class SummarizationAgent:
    """Produces a naive summary from transcript chunks."""

    def __init__(self, config: SummarizationConfig) -> None:
        self.config = config
        defensive_log("SummarizationAgent initialized with %s", self.config)

    def run(self, chunks: Iterable[List[str]]) -> List[str]:
        summaries: List[str] = []
        for chunk in chunks:
            text = " ".join(chunk)
            defensive_log("Summarizing chunk: %s", text)
            sentences = [s.strip() for s in text.split(".") if s.strip()]
            summary = ". ".join(sentences[: self.config.sentence_count])
            if summary and not summary.endswith('.'):
                summary += '.'
            summaries.append(summary)
        defensive_log("Summarization complete")
        return summaries
