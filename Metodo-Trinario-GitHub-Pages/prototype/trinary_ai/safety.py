from __future__ import annotations

from dataclasses import dataclass
import os
import shutil


@dataclass(frozen=True, slots=True)
class SystemStatus:
    cpu_count: int | None
    load_1m: float | None
    free_disk_bytes: int
    total_disk_bytes: int
    power_known: bool
    battery_percent: float | None
    on_external_power: bool | None
    risk_value: float
    message: str


class SafeHardwareMonitor:
    """Somente observação e recomendações; não altera hardware nem permissões."""

    def inspect(self, path: str = ".") -> SystemStatus:
        disk = shutil.disk_usage(path)
        load = None
        try:
            load = os.getloadavg()[0]
        except (AttributeError, OSError):
            pass

        battery_percent, plugged = self._read_linux_battery()
        power_known = battery_percent is not None

        disk_ratio = disk.free / disk.total if disk.total else 0.0
        risk = 0.0
        reasons: list[str] = []
        if disk_ratio < 0.05:
            risk -= 0.85
            reasons.append("espaço em disco crítico")
        elif disk_ratio < 0.15:
            risk -= 0.45
            reasons.append("espaço em disco baixo")

        if battery_percent is not None and plugged is False:
            if battery_percent < 10:
                risk -= 0.9
                reasons.append("bateria crítica e sem alimentação externa")
            elif battery_percent < 25:
                risk -= 0.5
                reasons.append("bateria baixa")

        risk = max(-0.95, min(0.95, risk))
        message = ", ".join(reasons) if reasons else "nenhum risco crítico detectado"
        return SystemStatus(
            cpu_count=os.cpu_count(),
            load_1m=load,
            free_disk_bytes=disk.free,
            total_disk_bytes=disk.total,
            power_known=power_known,
            battery_percent=battery_percent,
            on_external_power=plugged,
            risk_value=risk,
            message=message,
        )

    @staticmethod
    def _read_linux_battery() -> tuple[float | None, bool | None]:
        base = "/sys/class/power_supply"
        if not os.path.isdir(base):
            return None, None
        for name in os.listdir(base):
            folder = os.path.join(base, name)
            kind_file = os.path.join(folder, "type")
            try:
                with open(kind_file, encoding="utf-8") as handle:
                    if handle.read().strip() != "Battery":
                        continue
                with open(os.path.join(folder, "capacity"), encoding="utf-8") as handle:
                    percent = float(handle.read().strip())
                status = None
                status_file = os.path.join(folder, "status")
                if os.path.exists(status_file):
                    with open(status_file, encoding="utf-8") as handle:
                        status = handle.read().strip().lower()
                plugged = status in {"charging", "full"} if status else None
                return percent, plugged
            except (OSError, ValueError):
                continue
        return None, None
