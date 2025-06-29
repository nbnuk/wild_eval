import sys
import os
import pathlib
import importlib.util
from eval_framework import registered_evals

def import_eval_files_from(folder: str = "evals"):
    """Dynamically import all test_*.py files in the given folder."""
    path = pathlib.Path(folder)
    if not path.exists():
        print(f"⚠️  Eval folder '{folder}' does not exist.")
        return

    for py_file in path.glob("test_*.py"):
        module_name = py_file.stem
        module_path = py_file.resolve()
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

# --- Discover and import eval test files ---
import_eval_files_from("evals")

if __name__ == "__main__":
    for case in registered_evals:
        print(f"\n🔍 Running: {case.name}")
        results = case.run()
        for r in results:
            print(f"Input: {r['input']}")
            print(f"Expected: {r['expected']}")
            print(f"Output: {r['output']}")
            for scorer, score in r['scores'].items():
                print(f"{scorer}: {score:.2f}")
                extras = r['details'].get(scorer, {})
                for key, val in extras.items():
                    if key != "score":
                        print(f"  {key}: {val}")
            print("---")
