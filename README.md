# WildEval - Experimental AI Eval Framework for Biodiversity Data

A lightweight, local evaluation framework for biodiversity data AI tasks. This is an experimental codelab project for learning and inviting collaboration. 

## What Are Evals

Evals are like tests but for AI-powered apps, particularly LLM-powered applications. They help verify that your app is working as expected. While conventional tests typically return a simple pass or fail, evals provide a performance score that reflects how well your app is performing. The three-component structure (data, task, scorers) used in WildEval are directly inspired by [Braintrust's](https://www.braintrust.dev/) evaluation framework. 

## Features

- **Simple Test Definition**: Use Python decorators to define evaluation cases
- **Flexible Scoring**: Leverage [autoevals](https://github.com/braintrustdata/autoevals) comprehensive evaluation metrics or create custom scorers. The Autoevals suite (part of Braintrust) offers feature-rich scorers for string similarity, numeric comparison, JSON structure, and even LLM‑based evaluation.
- **Extensible**: Easy to add custom scorers and evaluation tasks
- **Local First**: Designed to run locally without external dependencies

    

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd wild-eval
```

### 2. Install Dependencies

This project uses `uv` for dependency management:

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# If uv sync doesn't work, you may need to install dependencies manually:
uv pip install autoevals requests openai
```

### 3. Install spaCy Model (needed to run NLP example evaluation)

```bash
python -m spacy download en_core_web_sm
```

### 4. Run Sample Evaluations

```bash
python run_eval.py
```

## Understanding Scorers

Scorers are functions that evaluate how well your AI task's output matches the expected result. They return a score (typically between 0-1 or 0-100) and optional metadata.

### Why Scorers Matter

Good evaluation metrics are crucial for:
- **Comparing different AI models** on the same task
- **Tracking improvements** as you iterate on your models
- **Understanding failure modes** and edge cases
- **Building confidence** in your AI systems




## Example Evals

WildEval has very simple example evals in the evals/ directory.  Their purpose is just to demonstrate the framework and help you get started.
Two interesting examples:
- `@eval_case("Redact Places with Spacy")` -  this eval evaluates a task that uses [spaCy](https://spacy.io/) for detecting and redacting place names in biodiversity data (it's very basic though!) It's in evals/eval_simple_examples.py. 
- `@eval_case("Redact Places with OpenAI")` - this eval evaluates a task that uses [OpenAI](https://openai.com/) to redact place names in biodiversity data. It also uses an LLM to evaluate the output. It's in evals/eval_openai_simple_example.py. 




## Creating Your Own Evaluations


Create a new Python file in the `evals/` directory with the naming pattern `eval_*.py`:

```python
# evals/eval_my_evaluation.py
from eval_framework import eval_case
from autoevals import Levenshtein

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
```

## Understanding the Eval Structure

Each eval has three components:

- **data**: A function that returns a list of test cases with `input` and `expected` values
- **task**: A function that processes the input and returns the output
- **scorers**: A list of scoring functions that compare output to expected results

## Available Scorers

### Autoevals Scorers
The framework is designed to work seamlessly with [autoevals](https://github.com/braintrustdata/autoevals), a comprehensive library of evaluation metrics. Autoevals provides many sophisticated scorers out of the box:

- **String Similarity**: `autoevals.Levenshtein`, `autoevals.StringSimilarity`
- **JSON Comparison**: JSON validation and structural comparison
- **Semantic Similarity**: `autoevals.SemanticSimilarity`, `autoevals.EmbeddingSimilarity`
- **LLM-based Evaluation**: `autoevals.LLMScorer`, `autoevals.Faithfulness`
- Check the [autoevals documentation](https://github.com/braintrustdata/autoevals) for the full list


#### Built-in Biodiversity Scorers
The framework could eventually include domain-specific scorers tailored to biodiversity tasks. For now, we’ve implemented a very simple example focused on location redaction, primarily to demonstrate the concept. 

- **`GazetteerMatchScorer`**: Checks if specific location names are present/absent in text (useful for location redaction tasks)


### Creating custom Scorers
You can create your own scorers by implementing a callable that returns a score:

```python
class MyCustomScorer:
    def __call__(self, output, expected):
        # Your scoring logic here
        score = calculate_score(output, expected)
        return {
            "score": score,
            "metadata": {"custom_info": "additional data"}
        }
```

## Configuration

### API Keys

For evaluations that use external APIs (like OpenAI), set your API keys:

```python
import openai
openai.api_key = "your-api-key-here"
```

Or use environment variables:
```bash
export OPENAI_API_KEY="your-api-key-here"
```



## Running Evals

#### Run All Evals
```bash
python run_eval.py
```

#### List Available Evals
```bash
python run_eval.py --list
```

#### Run Specific Eval
```bash
python run_eval.py --name "Simple Taxon Name Fix"
```

#### Run Evals by Pattern
```bash
python run_eval.py --filter "redact"    # Run all redaction-related evaluations
python run_eval.py --filter "name"      # Run all name-related evaluations
```

#### Get Help
```bash
python run_eval.py --help
```


## Key Dependencies

- Python 3.11+
- uv (package manager)
- autoevals (comprehensive evaluation metrics library)
- spaCy (for NLP features)
- requests (for API calls)
- openai (for OpenAI API integration)

## Learn More




### About autoevals

 [autoevals](https://github.com/braintrustdata/autoevals) is a comprehensive library of evaluation metrics developed by Braintrust, used by companies like Anthropic, OpenAI, and others in production environments. It provides standardized, well-tested evaluation functions that make it easy to assess AI model performance:

- **String Similarity**: Levenshtein distance, string similarity, exact matching
- **JSON Comparison**: JSON validation and structural comparison
- **Semantic Similarity**: Embedding-based similarity, semantic comparison
- **LLM-based Evaluation**: Using other LLMs to evaluate outputs (faithfulness, relevance, etc.)
- **Custom Metrics**: Framework for building domain-specific evaluation functions
- **Production Ready**: Used in real-world AI applications and thoroughly tested

### About spaCy

[spaCy](https://spacy.io/) is an open-source Python library for fast, industrial-strength Natural Language Processing (NLP). WildEval uses spaCy in a very simple example to detect and redact place names in biodiversity text, it's just enough to demonstrate what's possible. While spaCy is great for general-purpose NLP, many biodiversity tasks will benefit more from domain-specific models, such as those available on [Hugging Face](https://huggingface.co/).

spaCy provides tools like:

- **Named Entity Recognition (NER)**: Detect people, organizations, locations, dates, etc.
- **Tokenization**: Split text into words, sentences, etc.
- **Dependency parsing**: Understand grammatical relationships
- **Text classification**: Categorize text content
- **Similarity analysis**: Compare text meaning using word vectors

In biodiversity data contexts, spaCy could help with tasks like:
- Extracting species names from text descriptions
- Identifying geographic locations in observation records
- Parsing taxonomic hierarchies
- Analyzing field notes and descriptions


## License

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0e)
