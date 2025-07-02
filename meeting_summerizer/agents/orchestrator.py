from __future__ import annotations

import logging

from prefect import flow, task

from meeting_summerizer.agents.capture import CaptureAgent, CaptureConfig
from meeting_summerizer.agents.transcription import TranscriptionAgent, TranscriptionConfig
from meeting_summerizer.agents.storage import StorageAgent, StorageConfig
from meeting_summerizer.agents.chunking import ChunkingAgent, ChunkingConfig
from meeting_summerizer.agents.summarization import SummarizationAgent, SummarizationConfig
from meeting_summerizer.config import get_settings

logger = logging.getLogger(__name__)


defensive_log = logger.debug


@task
def capture_task(cfg: CaptureConfig):
    agent = CaptureAgent(cfg)
    return list(agent.run())


@task
def transcription_task(cfg: TranscriptionConfig, frames: list[bytes]):
    agent = TranscriptionAgent(cfg)
    return list(agent.run(frames))


@task
def storage_task(cfg: StorageConfig, transcripts: list[str]):
    defensive_log("Using DB url: %s", cfg.db_url)
    agent = StorageAgent(cfg)
    agent.run(transcripts)
    return agent.fetch_all()


@task
def chunking_task(cfg: ChunkingConfig, transcripts: list[str]):
    agent = ChunkingAgent(cfg)
    return list(agent.run(transcripts))


@task
def summarization_task(cfg: SummarizationConfig, chunks: list[list[str]]):
    agent = SummarizationAgent(cfg)
    return agent.run(chunks)


@flow
def orchestrator():
    settings = get_settings()
    defensive_log("Starting flow with settings %s", settings)
    frames = capture_task(CaptureConfig(meeting_id=settings.meeting_id))
    transcripts = transcription_task(TranscriptionConfig(), frames)
    stored = storage_task(StorageConfig(db_url=settings.db_url), transcripts)
    chunks = chunking_task(ChunkingConfig(), stored)
    summaries = summarization_task(SummarizationConfig(), chunks)
    for summary in summaries:
        logger.info("Summary: %s", summary)


if __name__ == "__main__":
    orchestrator()
