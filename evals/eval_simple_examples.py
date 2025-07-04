
import spacy

import requests
from eval_framework import eval_case
from autoevals import Levenshtein
from scorers import GazetteerMatchScorer


nlp = spacy.load("en_core_web_sm")

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
            {"input": "red fox", "expected": "Vulpes vulpes"}
        ],
        "task": nbn_name_match,
        "scorers": [Levenshtein()]
    }        
    
def redact_places(text):
    '''
    Redact places from the text - obviously a ludicrously simple implementation
    '''
    for place in ["Abersoch", "Bangor", "Llandudno", "Dolgellau", "Snowdonia"]:
        text = text.replace(place, "[REDACTED]")
    return text

@eval_case("Redact Places")
def test_redact_places():
    return {
        "data": lambda: [
            {"input": "Observed near Dolgellau in Snowdonia National Park.", "expected": "Observed near [REDACTED] in [REDACTED] National Park."},
            {"input": "Seen on a path near Abersoch", "expected": "Seen on a path near [REDACTED]"}
        ],
        "task": redact_places,
        "scorers": [GazetteerMatchScorer(["Abersoch", "Bangor", "Llandudno", "Dolgellau", "Snowdonia"])]
    }
    

    
def redact_with_spacy(text):
    doc = nlp(text)
    redacted = text
    for ent in doc.ents:
        if ent.label_ == "GPE":  # e.g., "Abersoch"
            redacted = redacted.replace(ent.text, "[REDACTED]")
    return redacted    
 
@eval_case("Redact Places with Spacy")
def test_redact_places_with_spacy():
    return {
        "data": lambda: [
            {"input": "Observed near Dolgellau in Snowdonia National Park.", "expected": "Observed near [REDACTED] in [REDACTED] National Park."},
            {"input": "Seen on a path near Abersoch", "expected": "Seen on a path near [REDACTED]"}
        ],
        "task": redact_with_spacy,
        "scorers": [GazetteerMatchScorer(["Abersoch", "Bangor", "Llandudno", "Dolgellau", "Snowdonia"])]
    }