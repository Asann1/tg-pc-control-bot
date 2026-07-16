"""
get_status.py — use case «получить статус ПК».

"""

from tg_pc_control_bot.infrastructure.metrics.psutil_metrics import PsutilMetricsGateway


class GetStatusUseCase:
    def __init__(self, metrics_gateway: PsutilMetricsGateway) -> None:
        self._metrics = metrics_gateway

    def execute(self) -> str:
        snapshot = self._metrics.get_snapshot()

        hours = snapshot.uptime_seconds // 3600
        minutes = (snapshot.uptime_seconds % 3600) // 60

        return (
            "🖥 Статус ПК:\n"
            f"💻 CPU: {round(snapshot.cpu_percent, 1)}%\n"
            f"📊 RAM: {round(snapshot.ram_percent, 1)}%\n"
            f"💽 Disk C: {round(snapshot.disk_percent, 1)}%\n"
            f"⏱ Uptime: {hours}ч {minutes}м\n"
            f"🌐 Network: ↑{round(snapshot.sent_mb, 1)} MB / ↓{round(snapshot.recv_mb, 1)} MB"
        )