from __future__ import annotations

import subprocess


class WindowsSystemGateway:
    def shutdown(self) -> tuple[bool, str]:
        return self._run_command(["shutdown", "/s", "/t", "10"])

    def restart(self) -> tuple[bool, str]:
        return self._run_command(["shutdown", "/r", "/t", "10"])

    def sleep(self) -> tuple[bool, str]:
        powershell = [
            "powershell",
            "-Command",
            "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)",
        ]
        return self._run_command(powershell)

    def _run_command(self, command: list[str]) -> tuple[bool, str]:
        try:
            completed = subprocess.run(command, capture_output=True, text=True, check=False)
            if completed.returncode == 0:
                return True, "ok"
            stderr = completed.stderr.strip() or completed.stdout.strip() or "Unknown system error."
            return False, stderr
        except Exception as exc:  # pragma: no cover
            return False, str(exc)
