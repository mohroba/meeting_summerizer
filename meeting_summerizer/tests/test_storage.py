import os

from meeting_summerizer.agents.storage import StorageAgent, StorageConfig


def test_storage(tmp_path):
    db_url = f"sqlite:///{tmp_path}/test.db"
    agent = StorageAgent(StorageConfig(db_url=db_url, session_id="s1"))
    agent.run([
        {"timestamp": 1, "text": "hello"},
        {"timestamp": 2, "text": "world"},
    ])
    rows = agent.fetch_all()
    assert rows == ["hello", "world"]
