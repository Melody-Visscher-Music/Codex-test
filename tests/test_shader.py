import types

from scripts import shader


class FakeNodes(dict):
    def clear(self):
        super().clear()

    def new(self, node_type):
        if node_type == "ShaderNodeEmission":
            node = types.SimpleNamespace(
                name="Emission",
                inputs={"Color": types.SimpleNamespace(default_value=[0, 0, 0, 0])},
                outputs={"Emission": object()},
            )
        else:
            node = types.SimpleNamespace(
                name="Material Output", inputs={"Surface": object()}, outputs={}
            )
        self[node.name] = node
        return node


class FakeNodeTree:
    def __init__(self):
        self.nodes = FakeNodes()
        self.links = types.SimpleNamespace(new=lambda *args, **kwargs: None)


class FakeMaterials(dict):
    def new(self, name):
        mat = types.SimpleNamespace(
            name=name, use_nodes=False, node_tree=FakeNodeTree()
        )
        self[name] = mat
        return mat


def test_create_emission_material(monkeypatch):
    fake_bpy = types.SimpleNamespace(
        data=types.SimpleNamespace(materials=FakeMaterials())
    )
    monkeypatch.setattr(shader, "bpy", fake_bpy)
    mat = shader.create_emission_material("MyMat", (0.2, 0.3, 0.4))
    emission = mat.node_tree.nodes["Emission"]
    color = emission.inputs["Color"].default_value
    assert tuple(color[:3]) == (0.2, 0.3, 0.4)
