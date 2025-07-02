from meeting_summerizer.agents.chunking import ChunkingAgent, ChunkingConfig


def test_chunking():
    agent = ChunkingAgent(ChunkingConfig(size=2))
    chunks = list(agent.run(["a", "b", "c"]))
    assert chunks == [["a", "b"], ["c"]]
