import types

from scripts import optimize


class MockModifiers:
    def __init__(self):
        self.created = []

    def new(self, name, type):
        mod = types.SimpleNamespace(name=name, type=type, ratio=1.0)
        self.created.append(mod)
        return mod


class MockObject:
    def __init__(self):
        self.modifiers = MockModifiers()


def test_decimate(monkeypatch):
    applied = {}
    fake_bpy = types.SimpleNamespace(
        ops=types.SimpleNamespace(
            object=types.SimpleNamespace(
                modifier_apply=lambda modifier: applied.setdefault("name", modifier)
            )
        )
    )
    monkeypatch.setattr(optimize, "bpy", fake_bpy)
    obj = MockObject()
    ratio = optimize.decimate_object(obj, 0.25, apply=True)
    assert obj.modifiers.created[0].ratio == 0.25
    assert applied["name"] == "Decimate"
    assert ratio == 0.25
