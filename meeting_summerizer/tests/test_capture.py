from meeting_summerizer.agents.capture import CaptureAgent, CaptureConfig


def test_capture():
    agent = CaptureAgent(CaptureConfig(meeting_id="id", frame_count=2))
    frames = list(agent.run())
    assert len(frames) == 2
