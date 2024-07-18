# output_parser.py

import json
import re

class OutputParser:
    @staticmethod
    def find_json(text: str) -> str:
        """
        Find the JSON block within the provided text.
        Args:
            text (str): The input text containing JSON.
        Returns:
            str: The JSON block as a string.
        """
        pattern = r"""```json(.*?)```"""
        matches = re.findall(pattern, text, re.DOTALL)
        if not matches:
            raise ValueError("No JSON block found in the provided text.")
        return matches[0]

    @staticmethod
    def json_to_list(json_code: str) -> list:
        """
        Convert a JSON string to a Python list.
        Args:
            json_code (str): The JSON string.
        Returns:
            list: The corresponding Python list.
        """
        parsed_json = json.loads(json_code)
        if isinstance(parsed_json, list):
            return parsed_json
        return parsed_json[next(iter(parsed_json))]

    @staticmethod
    def output_to_list(output: str) -> list:
        """
        Convert model output to a list of key phrases.
        Args:
            output (str): The model output containing JSON.
        Returns:
            list: The list of key phrases.
        """
        return OutputParser.json_to_list(OutputParser.find_json(output))
