"""
This is an example of a tools using the Ollama API.
We can inject user defined functions into the LLM.
And, based on the user prompt, the LLM can call the functions.

crysanthus@gmail.com
"""

import ollama

"""
Need: ollama local server running

LLM_TO_USE can be one of the following:
- llama3.2
- llama3.1
- qwen2.5-coder
"""
LLM_TO_USE = "qwen2.5-coder"


def add_two_numbers(a: int, b: int) -> int:
	"""
	Adds two numbers together.
	
	Args:
		a (int): The first number.
		b (int): The second number.
	
	Returns:
		int: The sum of the two numbers.
	"""
	return a + b


def subtract_two_numbers(a: int, b: int) -> int:
	"""
	Subtracts two numbers together.
	
	Args:
		a (int): The first number.
		b (int): The second number.
	
	Returns:
		int: The difference of the two numbers.
	"""
	return a - b


def multiply_two_numbers(a: int, b: int) -> int:
	"""
	Multiplies two numbers together.
	
	Args:
		a (int): The first number.
		b (int): The second number.
	
	Returns:
		int: The product of the two numbers.
	"""
	return a * b


def divide_two_numbers(a: int, b: int) -> int:
	"""
	Divides two numbers together.
	
	Args:
		a (int): The first number.
		b (int): The second number.
	
	Returns:
		int: The quotient of the two numbers.
	"""
	return a / b


available_functions = {
	"add_two_numbers": add_two_numbers,
	"subtract_two_numbers": subtract_two_numbers,
	"multiply_two_numbers": multiply_two_numbers,
	"divide_two_numbers": divide_two_numbers,
}

while True:
	"""
	Runs a chat session with the LLM.

	Can ask calculator questions in various ways, such as:
	- "What is 1 + 1?"
	- "Add 1 and 1"
	- "1 plus 1"
	- "one plus one"
	"""

	prompt = input("\n\nI am a calculator.\nAsk me a calculator question.\n`q` to exit.\n You: ")

	if prompt.lower().strip() == "q":
		break

	response = ollama.chat(
		LLM_TO_USE,
		messages=[
			{"role": "user", "content": prompt}
		],
		tools=[add_two_numbers, subtract_two_numbers, multiply_two_numbers, divide_two_numbers],
	)
	
	for tool in response.message.tool_calls or []:

		try:
			function_to_call = available_functions[tool.function.name]

		except KeyError:
			print(f'Function not found: {tool.function.name}')
			continue
		
		print(f'Function called: {tool.function.name}, Result: ', function_to_call(**tool.function.arguments))
