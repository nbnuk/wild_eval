from autoevals.string import Levenshtein as AELevenshtein
# from autoevals.string import StringSimilarity as AEStringSimilarity




class Levenshtein:
    def __call__(self, output, expected):
        result = AELevenshtein().eval(str(output), str(expected))      
        if result.metadata:
            return {
                "score": result.score,
                "metadata": result.metadata
            }
        else:
            return {
                "score": result.score
            }
            

class GazetteerMatchScorer:
    '''
    This simple scorer confirms whether location names were removed, but does not consider how the rest of the sentence was handled.
    '''
    def __init__(self, gazetteer: list[str]):
        self.gazetteer = gazetteer

    def __call__(self, output, expected):
        leaked = [place for place in self.gazetteer if place.lower() in output.lower()]
        return {
            "score": 0 if leaked else 1,
            "metadata": {"leaked_places": leaked}
        }


