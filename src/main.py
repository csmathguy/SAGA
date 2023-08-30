import os
from agent.git_agent import GitAgent  # Assuming your GitAgent class is in a file called git_agent.py
import logging
import config  # Import your config file

def main():
    logging.basicConfig(level=logging.INFO)

    git_agent = GitAgent(api_key=config.GIT_ACCESS_TOKEN, local_directory=os.getcwd())
    
    #setup_github_repository(git_agent,"csmathguy","SAGA", False)
    setup_branch_and_pr(git_agent, "AddGitBranch","Add Git Branching and PR creation to code-base", "Add Git Branch and PR Creation","Add Git Branch and PR Creation", "csmathguy", "SAGA")


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
