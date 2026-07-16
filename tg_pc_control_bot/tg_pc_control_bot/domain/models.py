from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetricsSnapshot:
    cpu_percent: float
    ram_percent: float
    disk_percent: float
    uptime_seconds: int
    sent_mb: float
    recv_mb: float


@dataclass(frozen=True)
class ProcessInfo:
    pid: int
    name: str
    cpu_percent: float
    ram_percent: float
