from meeting_summerizer.agents.transcription import (
    TranscriptionAgent,
    TranscriptionConfig,
)


def test_transcription():
    agent = TranscriptionAgent(TranscriptionConfig())
    result = list(agent.run([b"a", b"b"]))
    assert len(result) == 2
