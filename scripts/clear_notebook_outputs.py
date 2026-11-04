"""Clear outputs before committing; run from any directory."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for path in root.rglob("*.ipynb"):
    if ".ipynb_checkpoints" in path.parts:
        continue
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        cell["metadata"] = {}
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Cleared:", path.relative_to(root))
