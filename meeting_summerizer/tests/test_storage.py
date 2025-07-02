import os

from meeting_summerizer.agents.storage import StorageAgent, StorageConfig


def test_storage(tmp_path):
    db_url = f"sqlite:///{tmp_path}/test.db"
    agent = StorageAgent(StorageConfig(db_url=db_url))
    agent.run(["hello", "world"])
    rows = agent.fetch_all()
    assert rows == ["hello", "world"]
