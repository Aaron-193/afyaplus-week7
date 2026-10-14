from pathlib import Path
import sys

# Ensure imports resolve consistently whether pytest is launched from the repo root or a parent.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
