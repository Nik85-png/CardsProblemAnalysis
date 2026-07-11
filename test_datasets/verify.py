"""Quick validation of test CSVs using process_csv_to_json."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from process_dataset import process_csv_to_json

HERE = Path(__file__).resolve().parent

for name in ("test_small", "test_b_conditions"):
    path = str(HERE / f"{name}.csv")
    payload = process_csv_to_json(path)
    stats = payload["statistics"]
    conds = sorted(set(t["condition"] for t in payload["analysis_types"][5]["trials"]))
    print(f"{name}.csv: {stats['total_trials']} trials, "
          f"success_rate={stats['success_rate']}%, "
          f"conditions={conds}")

print("\nBoth test CSVs are valid!")
