import sys
import os
import pathlib
import importlib.util
import argparse
from eval_framework import registered_evals

def import_eval_files_from(folder: str = "evals"):
    """Dynamically import all eval_*.py files in the given folder."""
    path = pathlib.Path(folder)
    if not path.exists():
        print(f"⚠️  Eval folder '{folder}' does not exist.")
        return

    for py_file in path.glob("eval_*.py"):
        module_name = py_file.stem
        module_path = py_file.resolve()
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

def run_evaluations(filter_pattern=None, eval_case_name=None):
    """Run evaluations with optional filtering."""
    if not registered_evals:
        print("⚠️  No evaluations found. Make sure you have eval_*.py files in the evals/ directory.")
        return

    # Filter evaluations if specified
    eval_cases_to_run = []
    for eval_case in registered_evals:
        if eval_case_name and eval_case.name.lower() != eval_case_name.lower():
            continue
        if filter_pattern and filter_pattern.lower() not in eval_case.name.lower():
            continue
        eval_cases_to_run.append(eval_case)

    if not eval_cases_to_run:
        if eval_case_name:
            print(f"⚠️  No evaluation found with name '{eval_case_name}'")
        elif filter_pattern:
            print(f"⚠️  No evaluations found matching '{filter_pattern}'")
        else:
            print("⚠️  No evaluations to run")
        return

    for eval_case in eval_cases_to_run:
        print(f"\n🔍 Running: {eval_case.name}")
        results = eval_case.run()
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

def list_evaluations():
    """List all available evaluations."""
    if not registered_evals:
        print("⚠️  No evaluations found. Make sure you have eval_*.py files in the evals/ directory.")
        return

    print("📋 Available evaluations:")
    for i, eval_case in enumerate(registered_evals, 1):
        print(f"  {i}. {eval_case.name}")

# --- Discover and import eval files ---
import_eval_files_from("evals")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="WildEval - Run biodiversity data AI evaluations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_eval.py                    # Run all evaluations
  python run_eval.py --list            # List all available evaluations
  python run_eval.py --name "Species Name Correction"  # Run specific evaluation
  python run_eval.py --filter "redact" # Run evaluations containing "redact"
  python run_eval.py --filter "name"   # Run evaluations containing "name"
        """
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available evaluations"
    )
    
    parser.add_argument(
        "--name", "-n",
        type=str,
        help="Run a specific evaluation by exact name"
    )
    
    parser.add_argument(
        "--filter", "-f",
        type=str,
        help="Run evaluations whose names contain this pattern (case-insensitive)"
    )

    args = parser.parse_args()

    if args.list:
        list_evaluations()
    else:
        run_evaluations(filter_pattern=args.filter, eval_case_name=args.name)
