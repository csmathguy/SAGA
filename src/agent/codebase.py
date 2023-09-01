import os

class CodebaseAgent:
    
    def __init__(self, repository_path: str):
        self.repo_path = repository_path

    def get_directory_structure(self, start_path=None, exclusions=None) -> dict:
        """
        Get the directory structure starting from `start_path` or the root of the repository.

        Parameters:
            start_path (str): The path to start scanning from. Defaults to the root of the repository.
            exclusions (list): List of folder or filenames to exclude.
        
        Returns:
            dict: A dictionary representing the directory structure.
        """
        if start_path is None:
            start_path = self.repo_path

        if exclusions is None:
            exclusions = []

        dir_structure = {}
        start_path_parts = start_path.split(os.sep)

        for root, dirs, files in os.walk(start_path):
            # Exclude directories and files in the exclusions list
            dirs[:] = [d for d in dirs if d not in exclusions]
            files = [f for f in files if f not in exclusions]

            subtree = {}
            for d in dirs:
                subtree[d] = {}
            for f in files:
                subtree[f] = None  # Files are leaves, hence mapped to None

            path_parts = root.split(os.sep)

            # Skip the parts of the path that are common with start_path
            relative_parts = path_parts[len(start_path_parts):]

            parent_dir_subtree = dir_structure
            for part in relative_parts:
                parent_dir_subtree = parent_dir_subtree.setdefault(part, {})
            parent_dir_subtree.update(subtree)

        return dir_structure
