"""Comprehensive Blender scripting utilities.

Combines exporting, optimization, shader creation, and animation helpers
into a single module. All operations support a ``dry_run`` flag to avoid
unexpected modifications when run outside Blender.
"""

from __future__ import annotations

import os
from typing import Iterable, List, Mapping, Sequence, Tuple

try:  # pragma: no cover - covered via tests using mock bpy
    import bpy
except ModuleNotFoundError:  # pragma: no cover
    bpy = None  # type: ignore


# ---------------------------------------------------------------------------
# Selection helpers


def _select_objects(names: Iterable[str]) -> None:
    for obj in bpy.data.objects:
        obj.select_set(obj.name in names)


# ---------------------------------------------------------------------------
# Export utilities


def batch_export(
    objects: Iterable[str],
    directory: str,
    formats: Sequence[str] = ("FBX", "GLTF"),
    apply_modifiers: bool = True,
    include_textures: bool = True,
    dry_run: bool = False,
) -> List[str]:
    """Export *objects* to *directory* for each format in *formats*.

    Supported formats: ``"FBX"`` and ``"GLTF"``. Returns list of written
    file paths.
    """

    paths: List[str] = []
    formats = [fmt.upper() for fmt in formats]
    for fmt in formats:
        ext = {"FBX": "fbx", "GLTF": "gltf"}.get(fmt)
        if ext is None:
            raise ValueError(f"Unsupported format: {fmt}")
        filepath = os.path.join(directory, f"export.{ext}")
        paths.append(filepath)
        if dry_run or bpy is None:
            print(f"[DRY RUN] Would export {list(objects)} to {filepath}")
            continue
        os.makedirs(directory, exist_ok=True)
        _select_objects(objects)
        if fmt == "FBX":
            bpy.ops.export_scene.fbx(
                filepath=filepath,
                use_selection=True,
                apply_unit_scale=True,
                apply_scale_options="FBX_SCALE_UNITS",
                bake_space_transform=True,
                object_types={"ARMATURE", "MESH"},
                use_mesh_modifiers=apply_modifiers,
                path_mode="COPY",
                embed_textures=include_textures,
            )
        else:  # GLTF
            bpy.ops.export_scene.gltf(
                filepath=filepath,
                export_selected=True,
                export_apply=apply_modifiers,
                export_texcoords=True,
                export_normals=True,
                export_draco_mesh_compression_enable=False,
            )
    return paths


# ---------------------------------------------------------------------------
# Optimization helpers


def optimize_object(
    obj,
    decimate_ratio: float = 0.5,
    apply_decimate: bool = True,
    triangulate: bool = False,
    shade_smooth: bool = True,
    dry_run: bool = False,
) -> Mapping[str, float]:
    """Apply common mesh optimizations to *obj*.

    Returns a mapping of applied settings.
    """

    result = {
        "decimate_ratio": decimate_ratio,
        "triangulate": triangulate,
        "shade_smooth": shade_smooth,
    }
    if dry_run or bpy is None:
        print(f"[DRY RUN] Would optimize {getattr(obj, 'name', obj)}: {result}")
        return result
    modifier = obj.modifiers.new(name="Decimate", type="DECIMATE")
    modifier.ratio = decimate_ratio
    if apply_decimate:
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    if triangulate:
        tri = obj.modifiers.new(name="Triangulate", type="TRIANGULATE")
        bpy.ops.object.modifier_apply(modifier=tri.name)
    if shade_smooth:
        bpy.ops.object.shade_smooth()
    return result


# ---------------------------------------------------------------------------
# Shader utilities


def create_principled_material(
    name: str,
    base_color: Sequence[float] = (1.0, 1.0, 1.0, 1.0),
    texture_path: str | None = None,
    emission_strength: float = 0.0,
    metallic: float = 0.0,
    roughness: float = 0.5,
):
    """Create a material using Principled BSDF and optional texture/emission."""

    if bpy is None:
        raise RuntimeError("bpy unavailable")
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    principled = nodes.new("ShaderNodeBsdfPrincipled")
    principled.inputs["Base Color"].default_value = base_color
    principled.inputs["Metallic"].default_value = metallic
    principled.inputs["Roughness"].default_value = roughness
    principled.inputs["Emission Strength"].default_value = emission_strength
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])
    if texture_path:
        tex = nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(texture_path)
        links.new(tex.outputs["Color"], principled.inputs["Base Color"])
    return mat


# ---------------------------------------------------------------------------
# Animation utilities


def apply_location_keyframes(
    obj,
    frames: Iterable[int],
    locations: Iterable[Sequence[float]],
    dry_run: bool = False,
) -> List[Tuple[int, Sequence[float]]]:
    """Insert location keyframes for *obj*.

    Returns a list of ``(frame, location)`` tuples."""

    data = list(zip(frames, locations))
    if dry_run or bpy is None:
        return data
    for frame, loc in data:
        obj.location = loc
        obj.keyframe_insert(data_path="location", frame=frame)
    return data


def retarget_animation(
    source,
    target,
    bone_map: Mapping[str, str],
    dry_run: bool = False,
) -> Mapping[str, str]:
    """Copy transforms from *source* bones to *target* using *bone_map*."""

    if dry_run or bpy is None:
        print(f"[DRY RUN] Would retarget using {bone_map}")
        return bone_map
    action = source.animation_data.action
    start, end = map(int, action.frame_range)
    for frame in range(start, end + 1):
        bpy.context.scene.frame_set(frame)
        for src_name, dst_name in bone_map.items():
            src = source.pose.bones.get(src_name)
            dst = target.pose.bones.get(dst_name)
            if not (src and dst):
                continue
            dst.location = src.location
            dst.rotation_quaternion = src.rotation_quaternion
            dst.scale = src.scale
            for path in ("location", "rotation_quaternion", "scale"):
                dst.keyframe_insert(data_path=path, frame=frame)
    return bone_map
