from agent.git_agent import GitAgent  # Assuming your GitAgent class is in a file called git_agent.py
import logging
import config  # Import your config file

def main():
    logging.basicConfig(level=logging.INFO)

    git_agent = GitAgent(api_key=config.GIT_ACCESS_TOKEN, local_directory="/")
    
    setup_github_repository(git_agent,"csmathguy","SAGA", False)
    
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
