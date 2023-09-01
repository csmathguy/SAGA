import os
import sys
import unittest
from unittest import TestCase, mock
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.agent.gpt_agent import GPTAgent, Role

class GPTAgentTest(TestCase):

    def setUp(self):
        self.gpt_agent = GPTAgent(api_key='fake_token', role=Role.JOKESTER, enable_memory=False)

    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data="System prompt for programmer.")
    def test_load_system_prompt(self, mock_file):
        role = Role.PROGRAMMER
        prompt = self.gpt_agent._load_system_prompt(role)
        mock_file.assert_called()
        self.assertEqual(prompt, "System prompt for programmer.")

    @mock.patch('requests.post')
    def test_ask_query(self, mock_post):
        mock_response = {
            'choices': [{
                'message': {
                    'content': 'Hello, world!'
                }
            }]
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.text = json.dumps(mock_response)

        response_content = self.gpt_agent.ask_query('Hello')
        self.assertEqual(response_content, 'Hello, world!')

    def test_parse_response(self):
        mock_response = {
            'choices': [
                {'message': {'content': 'Sample response from GPT-4'}}
            ]
        }
        parsed_response = self.gpt_agent._parse_response(mock_response)
        self.assertEqual(parsed_response, 'Sample response from GPT-4')

if __name__ == '__main__':
    unittest.main()
