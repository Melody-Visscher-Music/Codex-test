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


class DummyProps:
    @staticmethod
    def BoolProperty(**kwargs):
        return kwargs.get("default")


bpy.props = DummyProps()
class DummyOperator:
    def __init__(self):
        self.reported = []

    def report(self, level, message):
        self.reported.append((level, message))


class DummyData:
    def __init__(self):
        self.meshes = []
        self.materials = []
        self.images = []


bpy.types = types.SimpleNamespace(Operator=DummyOperator)
bpy.data = DummyData()
bpy.types = types.SimpleNamespace(Operator=object)
main

sys.modules["bpy"] = bpy
