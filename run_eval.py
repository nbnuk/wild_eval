import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval_framework import registered_evals
import sample_eval.my_eval  # auto-registers

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
            print("---")
