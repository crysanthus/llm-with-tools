"""
This example demonstrates using Ollama's function injection for file management tasks.
The assistant can understand natural language commands to perform file operations.

Example commands:
- "Create a new file called example.txt with 'Hello World' in it"
- "List all Python files in the current directory"
- "Search for files containing the word 'test'"
- "Show me the size of all jpg files"

crysanthus@gmail.com
"""

import os
import glob
from typing import List, Dict, Union, Any
import ollama

LLM_TO_USE = "qwen2.5-coder"

def create_file(filename: str, content: str = "") -> Dict[str, Any]:
	"""
	Creates a new file with optional content.
	
	Args:
		filename (str): Name of the file to create
		content (str): Content to write to the file
	
	Returns:
		Dict[str, Any]: Result dictionary with status and data
	"""
	try:
		with open(filename, 'w') as f:
			f.write(content)
		return {
			"status": "success",
			"operation": "create_file",
			"data": {"filename": filename, "message": f"Successfully created file: {filename}"}
		}
	except Exception as e:
		return {
			"status": "error",
			"operation": "create_file",
			"data": {"filename": filename, "error": str(e)}
		}

def list_files(pattern: str = "*") -> Dict[str, Any]:
	"""
	Lists files matching the given pattern.
	
	Args:
		pattern (str): Glob pattern to match files (e.g., "*.py", "*.txt")
	
	Returns:
		Dict[str, Any]: Result dictionary with status and data
	"""
	files = glob.glob(pattern)
	return {
		"status": "success",
		"operation": "list_files",
		"data": {"pattern": pattern, "files": files}
	}

def search_in_files(search_term: str, file_pattern: str = "*") -> Dict[str, Any]:
	"""
	Searches for a term in files matching the pattern.
	
	Args:
		search_term (str): Term to search for
		file_pattern (str): Pattern of files to search in
	
	Returns:
		Dict[str, Any]: Result dictionary with status and data
	"""
	results = {}
	for filename in glob.glob(file_pattern):
		try:
			with open(filename, 'r') as f:
				lines = f.readlines()
				matches = [line.strip() for line in lines if search_term.lower() in line.lower()]
				if matches:
					results[filename] = matches
		except Exception:
			continue
	
	return {
		"status": "success",
		"operation": "search_in_files",
		"data": {
			"search_term": search_term,
			"pattern": file_pattern,
			"matches": results
		}
	}

def get_file_sizes(pattern: str = "*") -> Dict[str, Any]:
	"""
	Gets sizes of files matching the pattern.
	
	Args:
		pattern (str): Glob pattern to match files
	
	Returns:
		Dict[str, Any]: Result dictionary with status and data
	"""
	sizes = {}
	for filename in glob.glob(pattern):
		try:
			size_bytes = os.path.getsize(filename)
			sizes[filename] = {
				"bytes": size_bytes,
				"formatted": format_size(size_bytes)
			}
		except Exception:
			continue
	
	return {
		"status": "success",
		"operation": "get_file_sizes",
		"data": {
			"pattern": pattern,
			"files": sizes
		}
	}

def format_size(size_in_bytes: int) -> str:
	"""Helper function to format file sizes."""
	for unit in ['B', 'KB', 'MB', 'GB']:
		if size_in_bytes < 1024:
			return f"{size_in_bytes:.2f} {unit}"
		size_in_bytes /= 1024
	return f"{size_in_bytes:.2f} TB"

def format_output(result: Dict[str, Any]) -> str:
	"""
	Formats the result dictionary into a human-readable string.
	
	Args:
		result (Dict[str, Any]): Result dictionary from operation functions
	
	Returns:
		str: Formatted output string
	"""
	if result["status"] == "error":
		return f"Error in {result['operation']}: {result['data']['error']}"

	operation = result["operation"]
	data = result["data"]

	if operation == "create_file":
		return data["message"]
	
	elif operation == "list_files":
		if not data["files"]:
			return f"No files found matching pattern: {data['pattern']}"
		return "Files found:\n" + "\n".join(f"- {file}" for file in data["files"])
	
	elif operation == "search_in_files":
		if not data["matches"]:
			return f"No matches found for '{data['search_term']}' in files matching '{data['pattern']}'"
		output = []
		for filename, matches in data["matches"].items():
			output.append(f"\nIn {filename}:")
			output.extend(f"  {line}" for line in matches)
		return "\n".join(output)
	
	elif operation == "get_file_sizes":
		if not data["files"]:
			return f"No files found matching pattern: {data['pattern']}"
		output = ["File sizes:"]
		for filename, size_info in data["files"].items():
			output.append(f"- {filename}: {size_info['formatted']}")
		return "\n".join(output)
	
	return f"Unknown operation: {operation}"

def main():
	available_functions = {
		"create_file": create_file,
		"list_files": list_files,
		"search_in_files": search_in_files,
		"get_file_sizes": get_file_sizes
	}

	print("File Management Assistant")
	print("------------------------")
	print("Example commands:")
	print("- Create a new file called example.txt with 'Hello World' in it")
	print("- List all Python files in the current directory")
	print("- Search for files containing the word 'test'")
	print("- Show me the size of all jpg files")
	print("Enter 'q' to quit")

	while True:
		prompt = input("\nWhat would you like to do? ")
		
		if prompt.lower().strip() == "q":
			break

		response = ollama.chat(
			LLM_TO_USE,
			messages=[{"role": "user", "content": prompt}],
			tools=[create_file, list_files, search_in_files, get_file_sizes]
		)

		for tool in response.message.tool_calls or []:
			try:
				function_to_call = available_functions[tool.function.name]
				result = function_to_call(**tool.function.arguments)
				print("\n" + format_output(result))

			except KeyError:
				print(f'Function not found: {tool.function.name}')
			except Exception as e:
				print(f'Error executing {tool.function.name}: {str(e)}')

if __name__ == "__main__":
	main()
