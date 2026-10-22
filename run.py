
import runpy
from pathlib import Path

script = Path("src/detect_anomalies.py")

if not script.exists():
    raise FileNotFoundError(
        "Cannot find src/detect_anomalies.py"
    )

runpy.run_path(str(script), run_name="__main__")
