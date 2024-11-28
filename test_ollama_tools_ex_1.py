import unittest
import ollama
from ollama_tools_ex_1 import (
	add_two_numbers,
	subtract_two_numbers,
	multiply_two_numbers,
	divide_two_numbers,
	LLM_TO_USE
)

class TestOllamaCalculator(unittest.TestCase):
	def setUp(self):
		"""Set up test cases"""
		self.available_functions = {
			"add_two_numbers": add_two_numbers,
			"subtract_two_numbers": subtract_two_numbers,
			"multiply_two_numbers": multiply_two_numbers,
			"divide_two_numbers": divide_two_numbers,
		}
		self.test_cases = [
			{
				"prompt": "What is 5 plus 3?",
				"expected_function": "add_two_numbers",
				"expected_result": 8
			},
			{
				"prompt": "Multiply 4 and 6",
				"expected_function": "multiply_two_numbers",
				"expected_result": 24
			},
			{
				"prompt": "What is 10 minus 7?",
				"expected_function": "subtract_two_numbers",
				"expected_result": 3
			},
			{
				"prompt": "Divide 15 by 3",
				"expected_function": "divide_two_numbers",
				"expected_result": 5
			}
		]

	def test_function_results(self):
		"""Test if functions produce expected results"""
		self.assertEqual(add_two_numbers(5, 3), 8)
		self.assertEqual(multiply_two_numbers(4, 6), 24)
		self.assertEqual(subtract_two_numbers(10, 7), 3)
		self.assertEqual(divide_two_numbers(15, 3), 5)

	def test_llm_function_calls(self):
		"""Test if LLM correctly interprets prompts and calls appropriate functions"""
		for test_case in self.test_cases:
			with self.subTest(prompt=test_case["prompt"]):
				response = ollama.chat(
					LLM_TO_USE,
					messages=[{"role": "user", "content": test_case["prompt"]}],
					tools=[add_two_numbers, subtract_two_numbers, 
						   multiply_two_numbers, divide_two_numbers],
				)
				
				# Check if there are any tool calls
				self.assertTrue(
					response.message.tool_calls,
					f"No tool calls made for prompt: {test_case['prompt']}"
				)
				
				# Get the first tool call
				tool_call = response.message.tool_calls[0]
				
				# Verify correct function was called
				self.assertEqual(
					tool_call.function.name,
					test_case["expected_function"],
					f"Wrong function called for prompt: {test_case['prompt']}"
				)
				
				# Execute the function and verify result
				function_to_call = self.available_functions[tool_call.function.name]
				result = function_to_call(**tool_call.function.arguments)
				self.assertEqual(
					result,
					test_case["expected_result"],
					f"Wrong result for prompt: {test_case['prompt']}"
				)

if __name__ == '__main__':
	unittest.main()
