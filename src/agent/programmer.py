import json
from agent.codebase import CodebaseAgent
from agent.gpt_agent import GPTAgent, Role


class ProgrammerAgent:
    def __init__(self, codebase_repo_path, gpt_api_key):
        self.codebase_agent = CodebaseAgent(codebase_repo_path)
        self.gpt_agent = GPTAgent(api_key=gpt_api_key, role=Role.PROGRAMMER)

    def perform_task(self, task_description):
        # Step 1: Gather project info
        project_structure = self.codebase_agent.get_directory_structure()

        # Step 2: Ask GPTAgent for the code
        query = f"Given the project structure {project_structure}, {task_description}."
        response_content_str = self.gpt_agent.ask_query(query)

        # Deserialize the response
        response_content = json.loads(response_content_str)

        # Extract code from the response
        code_content = response_content.get('code', 'No code found')
        
        print(f"Generated Code: {code_content}")
        # Here you can add code to integrate the generated code into the codebase.