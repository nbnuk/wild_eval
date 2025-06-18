import requests
from eval_framework import eval_case
from scorers import Levenshtein

@eval_case("Simple Taxon Name Fix")
def test_name_fix():
    return {
        "data": lambda: [{"input": "Panthara leo", "expected": "Panthera leo"}],
        "task": lambda name: name.replace("Panthara", "Panthera"),
        "scorers": [Levenshtein()]
    }
    
def nbn_name_match(name: str) -> str:
    response = requests.get("https://namematching.nbnatlas.org/api/search", params={"q": name})
    data = response.json()
    if data.get("matchType") == "EXACT" or "scientificName" in data:
        return data["scientificName"]
    return ""

@eval_case("NBN Atlas Name Resolution")
def test_name_resolution():
    return {
        "data": lambda: [
            {"input": "Bumblebee", "expected": "Bombus"},
            {"input": "red fox", "expected": "Vulpes vulpes"},
            {"input": "branta canadnesis", "expected": "Branta canadensis"}
        ],
        "task": nbn_name_match,
        "scorers": [Levenshtein()]
    }    
 