import logging
import os
import subprocess
import requests
import json

class GitAgent:
    """Class for managing Git repositories."""

    def __init__(self, repository_url=None, local_directory=None, 
                 default_branch='main', api_key=None):
        """
        Initialize a GitAgent instance.

        Parameters:
            repository_url (str, optional): URL of the remote repository.
            local_directory (str, optional): Local directory where the repository 
                                             should be cloned.
            default_branch (str, optional): The default branch to work with. Defaults to 'main'.
            api_key (str, optional): API key for authentication. Defaults to None.
        """
        self.repository_url = repository_url
        self.local_directory = local_directory
        self.default_branch = default_branch
        self.api_key = api_key

    def create_github_repo(self, repo_name, private=True):
        """
        Create a new GitHub repository.

        Parameters:
            username (str): The GitHub username.
            repo_name (str): The name of the new repository.
            private (bool, optional): Whether the repository should be private. Defaults to True.

        Returns:
            str: The HTML URL of the created repository if successful, otherwise None.
        """
        
        # Build the URL endpoint for the GitHub API
        url = f'https://api.github.com/user/repos'
        
        # Set up the headers for API authentication
        headers = {
            'Authorization': f'BEARER {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Create the payload to be sent in the API request
        payload = {
            'name': repo_name,
            'private': private
        }

        # Send a POST request to GitHub API to create a new repository
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Check if the repository was successfully created
        if response.status_code == 201:
            return response.json()['html_url']
        else:
            logging.error(f'Failed to create repository. {response.text}')
            return None

    def check_repository_exists(self, username, repo_name):
        """
        Check if a GitHub repository exists.

        Parameters:
            username (str): The GitHub username.
            repo_name (str): The name of the repository.

        Returns:
            bool: True if repository exists, otherwise False.
        """
        
        url = f'https://api.github.com/repos/{username}/{repo_name}'
        
        headers = {
            'Authorization': f'BEARER {self.api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            logging.error(f'Failed to check repository existence. {response.text}')
            return False

    def initialize_local_repo(self):
        """Initialize a local Git repository."""
        if self.local_directory is None:
            logging.error("Local directory is not set.")
            return
        
        try:
            if not os.path.exists(os.path.join(self.local_directory, ".git")):
                subprocess.run(['git', 'init'], cwd=self.local_directory, check=True)
                logging.info("Successfully initialized local repository.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to initialize local repository: {e}")

    def add_files_to_index(self):
        """Add files to the Git index."""
        try:
            subprocess.run(['git', 'add', '.'], check=True)
            logging.info("Successfully added files to Git index.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to add files to Git index: {e}")

    def commit_changes(self, message='Initial commit'):
        """Commit changes to the local Git repository.

        Parameters:
            message (str): The commit message. Defaults to 'Initial commit'.
        """
        try:
            subprocess.run(['git', 'commit', '-m', message], check=True)
            logging.info("Successfully committed changes.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to commit changes: {e}")

    def create_or_rename_branch_to_main(self):
        """
        Create or rename the default branch to 'main'.
        """
        try:
            subprocess.run(['git', 'branch', '-M', 'main'], cwd=self.local_directory, check=True)
            logging.info("Successfully created or renamed branch to 'main'.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to create or rename branch to 'main': {e}")

    def add_remote_origin(self, github_url):
        """Add a remote origin to the local Git repository.

        Parameters:
            github_url (str): The URL of the remote GitHub repository.
        """
        try:
            subprocess.run(['git', 'remote', 'add', 'origin', github_url], check=True)
            logging.info(f"Successfully added remote origin: {github_url}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to add remote origin: {e}")

    def push_to_remote(self, branch='main'):
        """Push changes to the remote Git repository.

        Parameters:
            branch (str): The branch to push to. Defaults to 'main'.
        """
        try:
            subprocess.run(['git', 'push', '-u', 'origin', branch], check=True)
            logging.info(f"Successfully pushed to remote branch: {branch}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to push to remote: {e}")