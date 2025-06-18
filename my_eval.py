from eval_framework import eval_case
from scorers import Levenshtein

@eval_case("Simple Taxon Name Fix")
def test_name_fix():
    return {
        "data": lambda: [{"input": "Panthara leo", "expected": "Panthera leo"}],
        "task": lambda name: name.replace("Panthara", "Panthera"),
        "scorers": [Levenshtein()]
    }
 