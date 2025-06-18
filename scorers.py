# import Levenshtein

# def levenshtein_score(a: str, b: str) -> float:
#     dist = Levenshtein.distance(a, b)
#     max_len = max(len(a), len(b))
#     return 1.0 - dist / max_len if max_len > 0 else 1.0

# class Levenshtein:
#     def __call__(self, output, expected):
#         return levenshtein_score(str(output), str(expected))

from autoevals.string import Levenshtein as AELevenshtein
from autoevals.string import StringSimilarity as AEStringSimilarity

class Levenshtein:
    def __call__(self, output, expected):
        result = AELevenshtein().eval(output=str(output), expected=str(expected))
        return result.score



class StringSimilarity:
    def __init__(self, field: str):
        self.field = field
        self.sim = AEStringSimilarity()

    def __call__(self, output: dict, expected: dict) -> float:
        return self.sim.eval(
            output.get(self.field, ""),
            expected.get(self.field, "")
        ).score
