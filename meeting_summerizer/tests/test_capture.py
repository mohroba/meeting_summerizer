from meeting_summerizer.agents.capture import CaptureAgent, CaptureConfig


class _Resp:
    def __init__(self, frames: int) -> None:
        self.frames = frames

    def raise_for_status(self) -> None:
        pass

    def iter_content(self, chunk_size: int):
        for i in range(self.frames):
            yield f"frame{i}".encode()


def test_capture(monkeypatch):
    def fake_get(url, params=None, stream=False, timeout=0):
        return _Resp(2)

    monkeypatch.setattr("requests.get", fake_get)
    cfg = CaptureConfig(bbb_url="http://x", secret="s", meeting_id="id", frame_count=2)
    agent = CaptureAgent(cfg)
    frames = list(agent.run())
    assert len(frames) == 2
