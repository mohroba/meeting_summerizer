from meeting_summerizer.agents.summarization import (
    SummarizationAgent,
    SummarizationConfig,
)


def test_summarization():
    agent = SummarizationAgent(SummarizationConfig(sentence_count=1))
    summaries = agent.run([["hello world. this is a test."]])
    assert summaries == ["hello world."]
