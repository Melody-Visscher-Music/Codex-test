# SPDX-License-Identifier: MIT
"""In-memory scene graph used for testing planners."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Mesh:
    """Simple mesh representation."""

    name: str
    triangles: int


@dataclass
class Material:
    """Material placeholder."""

    name: str


@dataclass
class Object:
    """Scene object containing mesh and materials."""

    name: str
    mesh: Mesh | None = None
    materials: list[Material] = field(default_factory=list)


@dataclass
class Action:
    """Animation action with keyframes."""

    name: str
    keyframes: list[int] = field(default_factory=list)


@dataclass
class NlaStrip:
    """NLA strip referencing an action."""

    name: str
    action: Action


@dataclass
class Scene:
    """Container for scene objects and actions."""

    objects: list[Object] = field(default_factory=list)
    actions: list[Action] = field(default_factory=list)


def create_demo_scene() -> Scene:
    """Return a simple scene useful for tests."""
    mesh = Mesh("Cube", 12)
    mat = Material("Material")
    obj = Object("Cube", mesh, [mat])
    action = Action("Move", [0, 10, 20])
    return Scene([obj], [action])
