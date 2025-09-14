import types

from scripts import export


def test_export_fbx(monkeypatch):
    calls = {}
    fake_bpy = types.SimpleNamespace()
    obj = types.SimpleNamespace(name="Cube", select_set=lambda value: None)
    fake_bpy.data = types.SimpleNamespace(objects=[obj])
    fake_bpy.ops = types.SimpleNamespace(
        export_scene=types.SimpleNamespace(fbx=lambda **kwargs: calls.update(kwargs))
    )
    monkeypatch.setattr(export, "bpy", fake_bpy)
    path = export.export_fbx(["Cube"], "/tmp/test.fbx")
    assert path == "/tmp/test.fbx"
    assert calls["filepath"] == "/tmp/test.fbx"


def test_export_gltf(monkeypatch):
    calls = {}
    fake_bpy = types.SimpleNamespace()
    obj = types.SimpleNamespace(name="Cube", select_set=lambda value: None)
    fake_bpy.data = types.SimpleNamespace(objects=[obj])
    fake_bpy.ops = types.SimpleNamespace(
        export_scene=types.SimpleNamespace(gltf=lambda **kwargs: calls.update(kwargs))
    )
    monkeypatch.setattr(export, "bpy", fake_bpy)
    path = export.export_gltf(["Cube"], "/tmp/test.gltf")
    assert path == "/tmp/test.gltf"
    assert calls["filepath"] == "/tmp/test.gltf"
