import sys
from pathlib import Path
import types

if "ollama" not in sys.modules:
    mock = types.ModuleType("ollama")
    class _Resp:
        class M:
            content = "stub"
        message = M()
    mock.chat = lambda **_: _Resp()
    class _Client:
        def __init__(self, *a, **k):
            pass

        def chat(self, *a, **k):
            return _Resp()

    mock.Client = _Client
    sys.modules["ollama"] = mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
