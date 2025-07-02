import os
from meeting_summerizer.agents.orchestrator import orchestrator
from meeting_summerizer.agents.storage import StorageAgent, StorageConfig
import requests
import ollama
from websockets.sync.client import connect


class _Resp:
    def raise_for_status(self):
        pass

    def iter_content(self, chunk_size: int):
        for i in range(2):
            yield f"f{i}".encode()


class _WS:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def send(self, data: bytes) -> None:
        pass

    def recv(self) -> str:
        return '{"timestamp": 0, "text": "ok"}'


def test_orchestrator(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_URL", f"sqlite:///{tmp_path}/flow.db")
    monkeypatch.setenv("MEETING_ID", "test-meeting")
    monkeypatch.setenv("BBB_URL", "http://x")
    monkeypatch.setenv("BBB_SECRET", "s")
    monkeypatch.setenv("WHISPER_URL", "ws://w")
    monkeypatch.setenv("OLLAMA_MODEL", "llama2")
    monkeypatch.setenv("OLLAMA_HOST", "http://ollama")

    monkeypatch.setattr("requests.get", lambda *a, **k: _Resp())
    monkeypatch.setattr(
        "meeting_summerizer.agents.transcription.connect", lambda *a, **k: _WS()
    )
    class _Resp2:
        class M:
            content = "summary"

        message = M()

    monkeypatch.setattr("ollama.chat", lambda **k: _Resp2())

    orchestrator()
    agent = StorageAgent(
        StorageConfig(db_url=f"sqlite:///{tmp_path}/flow.db", session_id="test-meeting")
    )
    rows = agent.fetch_all()
    assert rows != []
