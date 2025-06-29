import openai
import os
from typing import Optional

import requests
from eval_framework import eval_case

openai.api_key = "YOUR_API_KEY"

def redact_places_with_openai(text):
    if not openai.api_key or openai.api_key == "YOUR_API_KEY":
        return "[SKIPPED: OpenAI API key not set]"
    prompt = f"""Redact any place names or geographic locations in this text by replacing them with [REDACTED]. Only redact location names.\n\nText: \"{text}\"\n"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

class LLMFidelityScorer:
    def __init__(self, model="gpt-3.5-turbo", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            self.api_key = None  # Don't raise exception, just set to None
        else:
            openai.api_key = self.api_key

    def __call__(self, output, expected):
        if not self.api_key:
            return {
                "score": 0.0,
                "metadata": {"status": "skipped", "reason": "OpenAI API key not set"}
            }
        
        prompt = f"""
You are an evaluator. Determine whether the second sentence is identical to the first, except that it has redacted geographic locations with [REDACTED].

Sentence A: {expected}
Sentence B: {output}

Answer with only one word: YES or NO.
"""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            reply = response.choices[0].message.content.strip().upper()
            return {
                "score": 1.0 if reply == "YES" else 0.0,
                "metadata": {
                    "model": self.model,
                    "raw_reply": reply
                }
            }
        except Exception as e:
            return {
                "score": 0.0,
                "metadata": {"error": str(e)}
            }

            
@eval_case("Redact Places with OpenAI")
def test_redact_places_with_openai():
    return {
        "data": lambda: [
            {"input": "Observed near Dolgellau in Snowdonia National Park.", "expected": "Observed near [REDACTED] in [REDACTED] National Park."},
            {"input": "Seen on a path near Abersoch", "expected": "Seen on a path near [REDACTED]"}
        ],
        "task": redact_places_with_openai,
        "scorers": [LLMFidelityScorer()]
    }
    
