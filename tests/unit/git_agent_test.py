import json
import os
import sys
from unittest import TestCase, mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.agent.git_agent import GitAgent

class GitAgentTest(TestCase):
    def setUp(self):
        self.git_agent = GitAgent(
            api_key="fake_api_key",
            local_directory="/fake/path",
        )

    @mock.patch('requests.post')
    def test_create_github_repo(self, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {'html_url': 'https://github.com/test/repo'}
        result = self.git_agent.create_github_repo('repo', True)
        self.assertEqual(result, 'https://github.com/test/repo')

    @mock.patch('requests.get')
    def test_check_repository_exists(self, mock_get):
        mock_get.return_value.status_code = 200
        exists = self.git_agent.check_repository_exists('test', 'repo')
        self.assertTrue(exists)

    @mock.patch('os.path.exists')
    @mock.patch('subprocess.run')
    def test_initialize_local_repo(self, mock_run, mock_exists):
        mock_exists.return_value = False
        self.git_agent.initialize_local_repo()
        mock_run.assert_called_with(['git', 'init'], cwd='/fake/path', check=True)

    @mock.patch('subprocess.run')
    def test_commit_changes(self, mock_run):
        self.git_agent.commit_changes('Initial commit')
        mock_run.assert_called_with(['git', 'commit', '-m', 'Initial commit'], check=True)
    
    @mock.patch('subprocess.run')
    def test_add_files_to_index(self, mock_run):
        self.git_agent.add_files_to_index()
        mock_run.assert_called_with(['git', 'add', '.'], check=True)
    
    @mock.patch('subprocess.run')
    def test_create_or_rename_branch_to_main(self, mock_run):
        self.git_agent.create_or_rename_branch_to_main()
        mock_run.assert_called_with(['git', 'branch', '-M', 'main'], cwd='/fake/path', check=True)

    @mock.patch('subprocess.run')
    def test_add_remote_origin(self, mock_run):
        self.git_agent.add_remote_origin('https://github.com/test/repo')
        mock_run.assert_called_with(['git', 'remote', 'add', 'origin', 'https://github.com/test/repo'], check=True)

    @mock.patch('subprocess.run')
    def test_push_to_remote(self, mock_run):
        self.git_agent.push_to_remote('main')
        mock_run.assert_called_with(['git', 'push', '-u', 'origin', 'main'], check=True)

    @mock.patch('subprocess.run')
    def test_create_new_branch(self, mock_run):
        self.git_agent.create_new_branch('feature')
        mock_run.assert_called_with(['git', 'checkout', '-b', 'feature'], cwd='/fake/path', check=True)

    @mock.patch('subprocess.run')
    def test_push_new_branch(self, mock_run):
        self.git_agent.push_new_branch('feature')
        mock_run.assert_called_with(['git', 'push', '-u', 'origin', 'feature'], cwd='/fake/path', check=True)

    @mock.patch('requests.post')
    def test_create_pull_request(self, mock_post):
        mock_post.return_value.status_code = 201
        username = 'username'
        test_repo = 'test_repo'

        self.git_agent.create_pull_request('main', 'feature', 'New Features', 'Added some new features.', username, test_repo)
        
        mock_post.assert_called_with(
            f'https://api.github.com/repos/{username}/{test_repo}/pulls',
            headers={
                'Authorization': f'BEARER fake_api_key',
                'Content-Type': 'application/json'
            },
            data=json.dumps({
                'title': 'New Features',
                'body': 'Added some new features.',
                'head': 'feature',
                'base': 'main'
            })
        )
