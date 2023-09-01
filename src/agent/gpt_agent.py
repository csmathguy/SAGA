from enum import Enum
import json
import os
import requests
from typing import Dict, List

class Role(Enum):
    """Enum class to define the roles that GPTAgent can take on."""
    PROGRAMMER = "programmer.txt"
    JOKESTER = "jokester.txt"

class GPTAgent:
    """Class to manage interactions with GPT-4."""

    def __init__(self, api_key: str, role: Role, enable_memory: bool = False):
        """
        Initialize the GPTAgent with a specific role and optional memory feature.

        Parameters:
            api_key (str): The API key for accessing GPT-4.
            role (Role): The role the agent should take on.
            enable_memory (bool): Whether to enable conversational memory. Defaults to False.
        """
        self.api_key = api_key
        self.system_prompt = self._load_system_prompt(role)
        self.prior_messages = []
        self.enable_memory = enable_memory

    def _load_system_prompt(self, role: Role) -> str:
        """
        Load the system prompt based on the role from a file.

        Parameters:
            role (Role): The role the agent should take on.

        Returns:
            str: The loaded system prompt.
        """
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, f"src\\agent\\system_prompts\\{role.value}")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")

        with open(file_path, "r") as f:
            return f.read()

    def ask_query(self, user_query: str) -> str:
        """
        Send a query to GPT-4 and return its response.

        Parameters:
            user_query (str): The query from the user.

        Returns:
            str: The response from GPT-4.
        """
        response = self._send_request_to_gpt(user_query)
        return self._parse_response(response)

    def _send_request_to_gpt(self, user_query: str) -> Dict:
        """
        Send a request to the GPT-4 API.

        Parameters:
            user_query (str): The query from the user.

        Returns:
            Dict: The response from the API, parsed as a dictionary.
        """
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        messages = [{'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': user_query}]

        if self.enable_memory:
            messages.extend(self.prior_messages)

        body = {'model': 'gpt-4', 'messages': messages}

        response = requests.post(url, headers=headers, json=body)
        return json.loads(response.text) if response.status_code == 200 else {'error': f'Error: {response.status_code}, {response.text}'}

    def _parse_response(self, response: Dict) -> str:
        """
        Parse the response from the GPT-4 API to extract the content.

        Parameters:
            response (Dict): The response from the API, parsed as a dictionary.

        Returns:
            str: The extracted content from the response.
        """
        content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
        return content
