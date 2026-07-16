from __future__ import annotations

import time

import psutil

from tg_pc_control_bot.domain.models import MetricsSnapshot, ProcessInfo


class PsutilMetricsGateway:
    def get_snapshot(self) -> MetricsSnapshot:
        network = psutil.net_io_counters()
        uptime = int(time.time() - psutil.boot_time())
        return MetricsSnapshot(
            cpu_percent=psutil.cpu_percent(interval=1),
            ram_percent=psutil.virtual_memory().percent,
            disk_percent=psutil.disk_usage("C:\\").percent,
            uptime_seconds=uptime,
            sent_mb=network.bytes_sent / 1024 / 1024,
            recv_mb=network.bytes_recv / 1024 / 1024,
        )

    def top_processes(self, limit: int = 5) -> list[ProcessInfo]:
        processes: list[ProcessInfo] = []
        for process in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            info = process.info
            processes.append(
                ProcessInfo(
                    pid=int(info["pid"]),
                    name=str(info["name"]),
                    cpu_percent=float(info["cpu_percent"] or 0.0),
                    ram_percent=float(info["memory_percent"] or 0.0),
                )
            )
        return sorted(processes, key=lambda p: (p.cpu_percent, p.ram_percent), reverse=True)[:limit]
