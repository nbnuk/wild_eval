
    
registered_evals = []   
    
    
class EvalCase:
    def __init__(self, name: str, data: Callable[[], List[Dict[str, Any]]], task: Callable, scorers: List[Callable]):
        self.name = name
        self.data = data
        self.task = task
        self.scorers = scorers
        registered_evals.append(self)

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

  


# for each test case you'd have to create a class like this:


class TestNameFix(EvalCase):
    def __init__(self):
        super().__init__("Test Name Fix", lambda: [{"input": "Panthara leo", "expected": "Panthera leo"}], lambda name: name.replace("Panthara", "Panthera"), [Levenshtein()])
        
# and then instantiate it in the main file:

test_name_fix = TestNameFix()

        
        
        
        