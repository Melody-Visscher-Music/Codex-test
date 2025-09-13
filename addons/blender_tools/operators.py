import bpy


class OBJECT_OT_hello(bpy.types.Operator):
    bl_idname = "object.hello"
    bl_label = "Say Hello"

    def execute(self, context):
        self.report({"INFO"}, "Hello World")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(OBJECT_OT_hello)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_hello)
