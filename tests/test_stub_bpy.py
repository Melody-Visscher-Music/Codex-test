import sys
import types

bpy = types.ModuleType("bpy")

class DummyOps:
    pass

class DummyUtils:
    def register_class(self, cls):
        pass

    def unregister_class(self, cls):
        pass

bpy.ops = DummyOps()
bpy.utils = DummyUtils()
bpy.types = types.SimpleNamespace(Operator=object)

sys.modules["bpy"] = bpy
