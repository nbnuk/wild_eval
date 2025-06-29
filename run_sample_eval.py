# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from eval_framework import registered_evals
# import sample_eval.simple_examples  # auto-registers the eval cases

# if __name__ == "__main__":
#     print("Running sample evaluations...")
#     for case in registered_evals:
#         print(f"\n🔍 Running: {case.name}")
#         results = case.run()
#         for r in results:
#             print(f"Input: {r['input']}")
#             print(f"Expected: {r['expected']}")
#             print(f"Output: {r['output']}")
#             for scorer, score in r['scores'].items():
#                 print(f"{scorer}: {score:.2f}")
#                 extras = r['details'].get(scorer, {})
#                 for key, val in extras.items():
#                     if key != "score":
#                         print(f"  {key}: {val}")
#             print("---") 