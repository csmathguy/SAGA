import json
import os
from agent.codebase import CodebaseAgent
from agent.git_agent import GitAgent  # Assuming your GitAgent class is in a file called git_agent.py
from agent.gpt_agent import GPTAgent, Role
import logging
from agent.programmer import ProgrammerAgent
import config  # Import your config file

def main():
    logging.basicConfig(level=logging.INFO)

    git_agent = GitAgent(api_key=config.GIT_ACCESS_TOKEN, local_directory=os.getcwd())
    
    #setup_github_repository(git_agent,"csmathguy","SAGA", False)
    #setup_branch_and_pr(git_agent, "AddGitBranch","Add Git Branching and PR creation to code-base", "Add Git Branch and PR Creation","Add Git Branch and PR Creation", "csmathguy", "SAGA")
    
    #ask_jokester_about_ai()
    #ask_programmer_for_algorithm()
    #create_branch_GPTAgent(git_agent)

    display_current_directory_structure()
    create_branch_CodebaseAgent(git_agent)

def programmer_testing():
    current_directory = os.getcwd()
    programmer_agent = ProgrammerAgent(codebase_repo_path=f"{current_directory}/output", gpt_api_key=config.CHATGPT_ACCESS_TOKEN)
    programmer_agent.perform_task("create a function that sorts an array")

def display_current_directory_structure():
    # Initialize the CodebaseAgent with the current working directory
    current_directory = os.getcwd()
    agent = CodebaseAgent(current_directory)
    structure = agent.get_directory_structure(exclusions=["__pycache__", "venv",".git", "objects"])
    
    # Use JSON.dumps for pretty-printing the dictionary
    print("Directory Structure of Current Working Directory:")
    print(json.dumps(structure, indent=4))

def ask_jokester_about_ai():
    # Initialize GPTAgent with JOKESTER role
    jokester_agent = GPTAgent(api_key=config.CHATGPT_ACCESS_TOKEN, role=Role.JOKESTER)
    
    # Send a query about "AI"
    query = "Tell me a joke about AI."
    response_content_str = jokester_agent.ask_query(query)
    
    # Deserialize the string into a Python dictionary
    response_content = json.loads(response_content_str)
    
    # Now this should work
    joke_content = response_content.get('joke', 'No joke found')
    answer_content = response_content.get('answer', 'No answer found')
    
    print(f"Joke: {joke_content}\nAnswer: {answer_content}")

def ask_programmer_for_algorithm():
    # Initialize GPTAgent with PROGRAMMER role
    programmer_agent = GPTAgent(api_key=config.CHATGPT_ACCESS_TOKEN, role=Role.PROGRAMMER)

    # Send a query about "Sorting Algorithm"
    query = "Can you provide a Python code snippet for a bubble sort algorithm?"
    response_content_str = programmer_agent.ask_query(query)

    # Deserialize the string into a Python dictionary
    # Note: This step may not be necessary if ask_query() returns a string directly
    response_content = json.loads(response_content_str) if isinstance(response_content_str, str) else response_content_str

    # Now this should work
    code_content = response_content.get('code', 'No code found')

    print(f"Code: {code_content}")

def setup_branch_and_pr(git_agent, branch_name, commit_message, pr_title, pr_description, username, repository):
    # Create and switch to a new feature branch
    git_agent.create_new_branch(branch_name)

    # Add files and commit changes (you already have methods for these)
    git_agent.add_files_to_index()
    git_agent.commit_changes(commit_message)

    # Push new feature branch to remote
    git_agent.push_new_branch(branch_name)

    # Create a pull request
    git_agent.create_pull_request(git_agent.default_branch, branch_name, pr_title, pr_description, username, repository)

def create_branch_GPTAgent(git_agent):
    """Get details for git operations like commit message, PR title, and PR description.

    Returns:
        tuple: A tuple containing commit message, PR title, PR description, username, repository, and branch name.
    """
    branch_name = "feature/add-GPTAgent-and-roles"
    commit_message = "Add GPTAgent class, role-based system prompts, and unit tests"
    pr_title = "Implement GPTAgent Class with Role-based System Prompts and Unit Tests"
    pr_description = """## Summary
    This PR implements the `GPTAgent` class, a utility for interacting with the GPT-4 API. The class is designed to be role-based, meaning it can adapt its behavior and queries based on the specified role (e.g., Programmer, Jokester).
    ## Changes
    - Add `GPTAgent` class with methods for loading system prompts, sending queries, and parsing responses.
    - Add `Role` enum class to define the roles that the `GPTAgent` can take on.
    - Add system prompt files `programmer.txt` and `jokester.txt` for respective roles.
    - Add unit tests for testing all the functionalities of `GPTAgent`.
    ## How to Test
    1. Run the unit tests to ensure all functionalities are working as expected.
    2. Manually test the `GPTAgent` class by initializing it with different roles and queries.
    ## Impact
    This PR sets the foundation for role-based interactions with the GPT-4 API, enabling more dynamic and context-aware queries and responses."""

    username = "csmathguy"
    repository = "SAGA"
    

    setup_branch_and_pr(git_agent, branch_name, commit_message, pr_title, pr_description, username, repository)

def create_branch_CodebaseAgent(git_agent):
    """Get details for git operations like commit message, PR title, and PR description.

    Returns:
        tuple: A tuple containing commit message, PR title, PR description, username, repository, and branch name.
    """
    branch_name = "feature/add-CodebaseAgent-functionality"
    commit_message = "Add get_directory_structure method in CodebaseAgent"
    pr_title = "Implement get_directory_structure in CodebaseAgent Class"
    pr_description = """## Summary
    This PR implements the `get_directory_structure` method in `CodebaseAgent`. This method provides an efficient way to get the directory structure starting from a given path.
    ## Changes
    - Add `get_directory_structure` method in `CodebaseAgent`.
    - Add unit tests for `get_directory_structure`.
    ## How to Test
    Run the unit tests to ensure all functionalities are working as expected.
    ## Impact
    This PR adds a key functionality to the `CodebaseAgent` class."""

    username = "csmathguy"
    repository = "SAGA"
    
    setup_branch_and_pr(git_agent, branch_name, commit_message, pr_title, pr_description, username, repository)



def setup_github_repository(git_agent, username, repo_name, private):
    """Set up a GitHub repository.

    Parameters:
        git_agent (GitAgent): The GitAgent instance.
        username (str): The GitHub username.
        repo_name (str): The name of the GitHub repository.
        private (bool): Whether the repository should be private.
    """
    if not git_agent.check_repository_exists(username, repo_name):
        github_url = git_agent.create_github_repo(repo_name, private)
        if github_url:
            logging.info(f"Successfully created repository at {github_url}")
            git_agent.initialize_local_repo()
            git_agent.add_files_to_index()
            git_agent.commit_changes()
            git_agent.create_or_rename_branch_to_main()
            git_agent.add_remote_origin(github_url)
            git_agent.push_to_remote()
        else:
            logging.error("Failed to create repository.")

if __name__ == '__main__':
    main()
