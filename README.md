# Blog Post (https://crysanthus.blogspot.com/2024/11/building-intelligent-calculator-with.html)

# llm-with-tools
In this blog post, I explore how to create an intelligent calculator by leveraging Ollama's API and function injection capabilities. This implementation showcases how Large Language Models (LLMs) can be enhanced with custom functions to perform specific tasks.

# Overview
The code demonstrates a practical example of how to inject user-defined functions into an LLM, allowing it to understand natural language queries and execute appropriate mathematical operations. The implementation uses Ollama, a powerful framework for running large language models locally.

# Key Components

## 1. Required Setup
A local Ollama server must be running
The code supports multiple LLM options including:
> llama3.2
> llama3.1
> qwen2.5-coder (used in this example)

## 2. Core Mathematical Functions
The code implements four basic mathematical operations:

> - add_two_numbers(a, b)
> - subtract_two_numbers(a, b)
> - multiply_two_numbers(a, b)
> - divide_two_numbers(a, b)

Each function is well-documented with proper type hints and docstrings, making the code maintainable and self-explanatory.

## 3. Function Registry
The available functions are stored in a dictionary for easy access:

```python
available_functions = {
    "add_two_numbers": add_two_numbers,
    "subtract_two_numbers": subtract_two_numbers,
    "multiply_two_numbers": multiply_two_numbers,
    "divide_two_numbers": divide_two_numbers,
}
```
## 4. Interactive Chat Loop
The program runs in an interactive loop where:

Users can input mathematical questions in natural language
The LLM interprets the question and selects the appropriate function
The selected function is executed with the parsed parameters
Results are displayed to the user
Usage Examples
The calculator can understand various forms of input:

* "What is 1 + 1?"
* "Add 1 and 1"
* "1 plus 1"
* "one plus one"
This flexibility in input processing demonstrates the power of using LLMs for natural language understanding.

# Technical Implementation Details
The core of the implementation uses Ollama's chat API with function injection:

```python
response = ollama.chat(
    LLM_TO_USE,
    messages=[{"role": "user", "content": prompt}],
    tools=[add_two_numbers, subtract_two_numbers, multiply_two_numbers, divide_two_numbers],
)
```

The LLM processes the user's input and determines which function to call along with the appropriate arguments. The program then executes the function and displays the result.

## Benefits and Applications
This implementation demonstrates several key concepts:

> Function Injection: How to extend LLM capabilities with custom functions
> Natural Language Processing: Converting human language to programmatic function calls
> Error Handling: Graceful handling of undefined functions and invalid inputs
> User Interface: Simple but effective interactive interface

