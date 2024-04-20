#!/usr/bin/python3
"""all unittests for console.py and all features"""
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand


class TestConsoleFeatures(unittest.TestCase):

    def test_help_show_command(self):
        """patch the stdout"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            HBNBCommand().onecmd("help show")
            self.assertNotEqual(fake_out.getvalue(), '')

if __name__ == '__main__':
    unittest.main()
