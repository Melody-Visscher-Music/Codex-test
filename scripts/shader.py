"""Shader node tree builders."""

from __future__ import annotations

from typing import Sequence

try:
    import bpy
except ModuleNotFoundError:  # pragma: no cover
    bpy = None  # type: ignore


def create_emission_material(name: str, color: Sequence[float]):
    """Create an emission material with the given RGBA color."""
    if bpy is None:
        raise RuntimeError("bpy unavailable")
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*color, 1.0)
    output = nodes.new("ShaderNodeOutputMaterial")
    mat.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return mat
