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
                'scores': {
                    scorer.__class__.__name__: scorer(output, item['expected'])
                    for scorer in self.scorers
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
