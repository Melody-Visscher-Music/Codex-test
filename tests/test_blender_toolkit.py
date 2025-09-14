import pathlib
import sys
import types

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import scripts.blender_toolkit as blender_toolkit  # noqa: E402
from scripts import (apply_location_keyframes, batch_export,  # noqa: E402
                     create_principled_material, optimize_object,
                     retarget_animation)


def test_batch_export(monkeypatch, tmp_path):
    calls = {}
    fake_bpy = types.SimpleNamespace()
    obj = types.SimpleNamespace(name="Cube", select_set=lambda value: None)
    fake_bpy.data = types.SimpleNamespace(objects=[obj])
    fake_bpy.ops = types.SimpleNamespace(
        export_scene=types.SimpleNamespace(
            fbx=lambda **kw: calls.setdefault("fbx", kw),
            gltf=lambda **kw: calls.setdefault("gltf", kw),
        )
    )
    monkeypatch.setattr(blender_toolkit, "bpy", fake_bpy)
    paths = batch_export(["Cube"], tmp_path.as_posix(), ["FBX", "GLTF"])
    assert len(paths) == 2
    assert calls["fbx"]["filepath"].endswith("export.fbx")
    assert calls["gltf"]["filepath"].endswith("export.gltf")


def test_optimize_object(monkeypatch):
    applied = []
    fake_bpy = types.SimpleNamespace(
        ops=types.SimpleNamespace(
            object=types.SimpleNamespace(
                modifier_apply=lambda modifier: applied.append(modifier),
                shade_smooth=lambda: applied.append("shade"),
            )
        )
    )
    monkeypatch.setattr(blender_toolkit, "bpy", fake_bpy)

    class MockModifiers:
        def __init__(self):
            self.created = []

        def new(self, name, type):
            mod = types.SimpleNamespace(name=name, type=type, ratio=1.0)
            self.created.append(mod)
            return mod

    obj = types.SimpleNamespace(name="Cube", modifiers=MockModifiers())
    result = optimize_object(obj, triangulate=True)
    assert result["triangulate"] is True
    assert applied == ["Decimate", "Triangulate", "shade"]


def test_create_principled_material(monkeypatch):
    class FakeNodes(dict):
        def clear(self):
            super().clear()

        def new(self, node_type):
            if node_type == "ShaderNodeOutputMaterial":
                node = types.SimpleNamespace(inputs={"Surface": object()}, outputs={})
            elif node_type == "ShaderNodeBsdfPrincipled":
                node = types.SimpleNamespace(
                    inputs={
                        "Base Color": types.SimpleNamespace(default_value=[0, 0, 0, 0]),
                        "Metallic": types.SimpleNamespace(default_value=0),
                        "Roughness": types.SimpleNamespace(default_value=0),
                        "Emission Strength": types.SimpleNamespace(default_value=0),
                    },
                    outputs={"BSDF": object()},
                )
            else:  # ShaderNodeTexImage
                node = types.SimpleNamespace(outputs={"Color": object()}, image=None)
            self[node_type] = node
            return node

    class FakeNodeTree:
        def __init__(self):
            self.nodes = FakeNodes()
            self.links = types.SimpleNamespace(new=lambda *a, **k: None)

    class FakeMaterials(dict):
        def new(self, name):
            mat = types.SimpleNamespace(
                name=name, use_nodes=False, node_tree=FakeNodeTree()
            )
            self[name] = mat
            return mat

    fake_bpy = types.SimpleNamespace(
        data=types.SimpleNamespace(
            materials=FakeMaterials(), images=types.SimpleNamespace(load=lambda p: p)
        )
    )
    monkeypatch.setattr(blender_toolkit, "bpy", fake_bpy)
    mat = create_principled_material(
        "Mat", (0.1, 0.2, 0.3, 1), texture_path="tex.png", emission_strength=1.0
    )
    principled = mat.node_tree.nodes["ShaderNodeBsdfPrincipled"]
    assert tuple(principled.inputs["Base Color"].default_value[:3]) == (0.1, 0.2, 0.3)
    assert principled.inputs["Emission Strength"].default_value == 1.0


def test_apply_location_keyframes():
    obj = types.SimpleNamespace(
        location=(0, 0, 0),
        inserted=[],
        keyframe_insert=lambda data_path, frame: obj.inserted.append(
            (data_path, frame)
        ),
    )
    frames = [1, 2]
    locs = [(0, 0, 0), (1, 1, 1)]
    result = apply_location_keyframes(obj, frames, locs)
    assert result == list(zip(frames, locs))
    assert obj.inserted == [("location", 1), ("location", 2)]
    assert obj.location == (1, 1, 1)


def test_retarget_animation_dry_run(capsys):
    mapping = {"Bone": "Bone"}
    result = retarget_animation(None, None, mapping, dry_run=True)
    assert result == mapping
    captured = capsys.readouterr().out
    assert "Would retarget" in captured
