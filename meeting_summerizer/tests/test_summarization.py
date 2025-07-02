from meeting_summerizer.agents.summarization import (
    SummarizationAgent,
    SummarizationConfig,
)
import ollama


def test_summarization(monkeypatch):
    class _Resp:
        class M:
            content = "summary"

        message = M()

    monkeypatch.setattr("ollama.chat", lambda **k: _Resp())
    agent = SummarizationAgent(SummarizationConfig())
    summaries = agent.run([["hello world"]])
    assert summaries == ["summary"]
