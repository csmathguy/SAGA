import os
import sys
import unittest
from unittest import TestCase
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.agent.codebase import CodebaseAgent

class TestCodebaseAgent(TestCase):

    def setUp(self):
        self.agent = CodebaseAgent('tests/unit/codebaseFolderTest')  # Update this path to your actual test directory

    def test_get_directory_structure_full(self):
        expected_structure = {
            'file1.txt': None,
            'folder1': {
                'file2.txt': None,
            },
            'folder2': {
                'folder3': {
                    'file3.txt': None
                }
            }
        }

        self.assertEqual(self.agent.get_directory_structure(), expected_structure)

    def test_get_directory_structure_subdir(self):
        expected_structure = {
            'folder3': {
                'file3.txt': None
            }
        }
        self.assertEqual(self.agent.get_directory_structure('tests/unit/codebaseFolderTest/folder2'), expected_structure)

if __name__ == '__main__':
    unittest.main()
