from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CommandScope(str, Enum):
    READ = "read"
    OPS = "ops"
    DANGEROUS = "dangerous"


@dataclass(frozen=True)
class CommandSpec:
    name: str
    scope: CommandScope
    description: str
