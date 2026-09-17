import os
from dataclasses import dataclass

import psutil


@dataclass(frozen=True)
class ResourceSnapshot:
    """
    Snapshot resource proses Sophie.
    """

    memory_mb: float
    cpu_percent: float


class ResourceMonitor:
    """
    Resource monitor Sophie.

    Monitor ini mengukur resource proses Python
    yang sedang menjalankan Sophie.
    """

    def __init__(self) -> None:
        self.process = psutil.Process(
            os.getpid()
        )

    def snapshot(
        self,
        cpu_interval: float = 0.2,
    ) -> ResourceSnapshot:
        """
        Mengambil snapshot RAM dan CPU.
        """

        memory_bytes = (
            self.process.memory_info().rss
        )

        cpu_percent = (
            self.process.cpu_percent(
                interval=cpu_interval
            )
        )

        return ResourceSnapshot(
            memory_mb=memory_bytes / (
                1024 * 1024
            ),
            cpu_percent=cpu_percent,
        )

    def print_snapshot(
        self,
        label: str,
        baseline_mb: float | None = None,
    ) -> ResourceSnapshot:
        """
        Mengambil dan menampilkan snapshot.
        """

        snapshot = self.snapshot()

        if baseline_mb is None:
            print(
                f"{label:<24} "
                f"RAM: {snapshot.memory_mb:8.2f} MB | "
                f"CPU: {snapshot.cpu_percent:6.2f}%"
            )

        else:
            delta = (
                snapshot.memory_mb
                - baseline_mb
            )

            print(
                f"{label:<24} "
                f"RAM: {snapshot.memory_mb:8.2f} MB | "
                f"ΔRAM: {delta:+8.2f} MB | "
                f"CPU: {snapshot.cpu_percent:6.2f}%"
            )

        return snapshot