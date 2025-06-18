from biodiv_eval.eval_framework import eval_case
from biodiv_eval.scorers import Levenshtein

@eval_case("Simple Taxon Name Fix")
def test_name_fix():
    return {
        "data": lambda: [{"input": "Panthara leo", "expected": "Panthera leo"}],
        "task": lambda name: name.replace("Panthara", "Panthera"),
        "scorers": [Levenshtein()]
    }
    
    def nbn_name_match(name: str) -> str:
    response = requests.get("https://namematching.nbnatlas.org/partner.json", params={"q": name})
    data = response.json()
    if data.get("matchType") == "EXACT" or "scientificName" in data:
        return data["scientificName"]
    return ""

@eval_case("NBN Atlas Name Resolution")
def test_name_resolution():
    return {
        "data": lambda: [
            {"input": "Panthara leo", "expected": "Panthera leo"},
            {"input": "red fox", "expected": "Vulpes vulpes"},
            {"input": "branta canadnesis", "expected": "Branta canadensis"}
        ],
        "task": nbn_name_match,
        "scorers": [Levenshtein()]
    }
