# SPDX-License-Identifier: MIT
class Mesh: ...
class Material: ...

class Object:
    name: str
    mesh: Mesh | None
    materials: list[Material]

class Action:
    name: str
    keyframes: list[int]

class NlaStrip:
    name: str
    action: Action

class Scene:
    objects: list[Object]
    actions: list[Action]

def create_demo_scene() -> Scene: ...
