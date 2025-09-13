import sys
import types

bpy = types.ModuleType("bpy")


class DummyOperator:
    bl_idname = ""
    bl_label = ""

    def __init__(self):
        self.reported = []

    def report(self, level, message):
        self.reported.append((level, message))


class DummyPanel:
    pass


class DummyAddonPreferences:
    pass


class DummyPropertyGroup:
    pass


class DummyUtils:
    def register_class(self, cls):
        pass

    def unregister_class(self, cls):
        pass


class DummyProps:
    @staticmethod
    def BoolProperty(**kwargs):
        return kwargs.get("default")

    @staticmethod
    def StringProperty(**kwargs):
        return kwargs.get("default", "")

    @staticmethod
    def FloatProperty(**kwargs):
        return kwargs.get("default", 0.0)


class DummyNodeTree(list):
    def new(self, name):
        node = types.SimpleNamespace(name=name, inputs=[object()], outputs=[object()])
        self.append(node)
        return node

    def clear(self):
        self[:] = []


class DummyLinks(list):
    def new(self, output, input):
        self.append((output, input))


class DummyMaterial:
    def __init__(self, name):
        self.name = name
        self.users = 0
        self.use_nodes = False
        self.node_tree = types.SimpleNamespace(
            nodes=DummyNodeTree(), links=DummyLinks()
        )


class DummyCollection(list):
    def new(self, name):
        item = DummyMaterial(name)
        self.append(item)
        return item

    def remove(self, item):
        super().remove(item)


class DummyData:
    def __init__(self):
        self.meshes = DummyCollection()
        self.materials = DummyCollection()
        self.images = DummyCollection()
        self.actions = DummyCollection()


bpy.utils = DummyUtils()

bpy_types = types.ModuleType("bpy.types")
bpy_types.Operator = DummyOperator
bpy_types.Panel = DummyPanel
bpy_types.AddonPreferences = DummyAddonPreferences
bpy_types.PropertyGroup = DummyPropertyGroup
bpy.types = bpy_types
sys.modules["bpy.types"] = bpy_types

bpy_props = types.ModuleType("bpy.props")
bpy_props.BoolProperty = DummyProps.BoolProperty
bpy_props.StringProperty = DummyProps.StringProperty
bpy_props.FloatProperty = DummyProps.FloatProperty
bpy.props = bpy_props
bpy.ops = types.SimpleNamespace(
    uv=types.SimpleNamespace(
        smart_project=lambda **kwargs: None, pack_islands=lambda **kwargs: None
    )
)

sys.modules["bpy.props"] = bpy_props

bpy.data = DummyData()
bpy.context = types.SimpleNamespace(
    scene=types.SimpleNamespace(render=types.SimpleNamespace(engine="CYCLES"))
)

sys.modules["bpy"] = bpy
