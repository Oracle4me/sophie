import os
import time

import psutil
from PySide6.QtWidgets import QApplication

from app.ui.desktop import SophieDesktop


def main() -> None:
    app = QApplication.instance() or QApplication([])
    process = psutil.Process(os.getpid())

    baseline_mb = process.memory_info().rss / (1024 * 1024)
    print()
    print("========================================")
    print("      SOPHIE DESKTOP RESOURCE TEST")
    print("========================================")
    print(f"Qt baseline : {baseline_mb:.2f} MB")

    window = SophieDesktop()
    window.show()
    app.processEvents()
    time.sleep(1)

    desktop_mb = process.memory_info().rss / (1024 * 1024)
    print(f"Desktop shell: {desktop_mb:.2f} MB")
    print(f"Delta        : {desktop_mb - baseline_mb:+.2f} MB")

    window.close()
    app.processEvents()

    print("Desktop shell ditutup.")


if __name__ == "__main__":
    main()