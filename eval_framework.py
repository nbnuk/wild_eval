from typing import Callable, List, Dict, Any

class EvalCase:
    def __init__(self, name: str, data: Callable[[], List[Dict[str, Any]]], task: Callable, scorers: List[Callable]):
        self.name = name
        self.data = data
        self.task = task
        self.scorers = scorers

    def run(self):
        results = []
        for item in self.data():
            output = self.task(item['input'])
            result = {
                'input': item['input'],
                'expected': item['expected'],
                'output': output,
                "scores": {
                    scorer.__class__.__name__: extract_score(scored)
                    for scorer in self.scorers
                    if (scored := scorer(output, item["expected"])) is not None
                },
                "details": {
                    scorer.__class__.__name__: extract_full(scored)
                    for scorer in self.scorers
                    if (scored := scorer(output, item["expected"])) is not None
                }
            }
            results.append(result)
        return results

registered_evals = []

def eval_case(name):
    def decorator(fn):
        case_data = fn()
        case = EvalCase(
            name=name,            
            data=case_data['data'],
            task=case_data['task'],
            scorers=case_data['scorers']
        )
        registered_evals.append(case)
        return fn
    return decorator

def extract_score(result):
    if isinstance(result, (int, float)):
        return float(result)
    elif isinstance(result, dict) and "score" in result:
        return float(result["score"])
    elif hasattr(result, "score"):
        return float(result.score)
    return 0.0  # fallback

def extract_full(result):
    if isinstance(result, (int, float)):
        return {"score": float(result)}
    elif isinstance(result, dict):
        return result
    elif hasattr(result, "score"):
        return {"score": float(result.score), "metadata": getattr(result, "metadata", {})}
    return {"score": 0.0}
