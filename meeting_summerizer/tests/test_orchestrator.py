import os
from meeting_summerizer.agents.orchestrator import orchestrator
from meeting_summerizer.agents.storage import StorageAgent, StorageConfig


def test_orchestrator(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_URL", f"sqlite:///{tmp_path}/flow.db")
    monkeypatch.setenv("MEETING_ID", "test-meeting")
    orchestrator()
    agent = StorageAgent(StorageConfig(db_url=f"sqlite:///{tmp_path}/flow.db"))
    rows = agent.fetch_all()
    assert rows != []
