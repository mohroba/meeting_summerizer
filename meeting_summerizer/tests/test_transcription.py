from meeting_summerizer.agents.transcription import (
    TranscriptionAgent,
    TranscriptionConfig,
)


class _WS:
    def __init__(self):
        self.messages = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def send(self, data: bytes) -> None:
        self.messages.append(data)

    def recv(self) -> str:
        return '{"timestamp": 0, "text": "ok"}'


def test_transcription(monkeypatch):
    monkeypatch.setattr(
        "meeting_summerizer.agents.transcription.connect", lambda *a, **k: _WS()
    )
    agent = TranscriptionAgent(TranscriptionConfig())
    result = list(agent.run([b"a", b"b"]))
    assert result == [
        {"timestamp": 0, "text": "ok"},
        {"timestamp": 0, "text": "ok"},
    ]
