from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Dict, List, Tuple

Unit = Literal["mm", "inch"]
Axis = Literal["X", "Y", "Z"]

# 2D primitives for sketches
@dataclass(frozen=True)
class Line:
    kind: Literal["line"] = "line"
    frm: Tuple[float, float] = (0.0, 0.0)
    to: Tuple[float, float] = (0.0, 0.0)

@dataclass(frozen=True)
class Circle:
    kind: Literal["circle"] = "circle"
    center: Tuple[float, float] = (0.0, 0.0)
    radius: float = 1.0

SketchEntity = Line | Circle

# Constraints (subset v1)
@dataclass(frozen=True)
class ConDistance:
    kind: Literal["distance"] = "distance"
    a: str = ""  # entity id
    b: str = ""  # entity id
    value: float = 0.0
    unit: Unit = "mm"

@dataclass(frozen=True)
class ConDiameter:
    kind: Literal["diameter"] = "diameter"
    e: str = ""  # entity id
    value: float = 1.0
    unit: Unit = "mm"

Constraint = ConDistance | ConDiameter

# Features
@dataclass(frozen=True)
class Extrude:
    kind: Literal["extrude"] = "extrude"
    sketch_id: str = ""
    depth: float = 1.0
    unit: Unit = "mm"
    direction: Axis = "Z"
    op: Literal["new","cut","join"] = "new"

@dataclass(frozen=True)
class Chamfer:
    kind: Literal["chamfer"] = "chamfer"
    edges: List[str] = field(default_factory=list)
    offset: float = 1.0
    unit: Unit = "mm"

Feature = Extrude | Chamfer

@dataclass(frozen=True)
class Sketch:
    plane: Axis = "Z"
    # entity id -> entity
    entities: Dict[str, SketchEntity] = field(default_factory=dict)
    constraints: List[Constraint] = field(default_factory=list)

@dataclass(frozen=True)
class PartSpec:
    name: str
    params: Dict[str, float]
    sketches: Dict[str, Sketch]
    features: List[Feature]
