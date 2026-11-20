#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import os
import shutil
import subprocess
import tempfile
import unittest
import uuid
import zipfile

class TestBase(unittest.TestCase):
    """This is the base class that handles all common steps needed for a test run.
    These are:
    - set an h5p input file that is used as the skeleton
    - set an spreadsheet file for the word list
    - copy the original h5p file into a temp file and modify that one only
    - remote the temp h5p file
    - provide access to the json files to verify that the h5p package was built correctly
    - sets path constants that are required to access the asset files
    """

    this_dir = os.path.dirname(os.path.realpath(__file__))
    assets_dir = f'{this_dir}/assets'
    temp_dir = tempfile.gettempdir()
    exec_py = f'{this_dir}/../import-cards.py'

    def setUp(self) -> None:
        self.h5p_input_file = ''
        self.spreadsheet = '' 
        self.h5p_test_file = self.temp_dir + '/' + str(uuid.uuid4())[-12:] + '.h5p'
        return super().setUp()

    def tearDown(self) -> None:
        if os.path.exists(self.h5p_test_file):
            os.remove(self.h5p_test_file)
        return super().tearDown()

    def run_command(self, args={}) -> dict:
        """Run the cli command "python3 import-cards.py" with the cli arguments
        and the two files passed to that function. The result contains the
        exit code, the output to stdout and stderr.
        """
        # Copy the input file to the temp.
        shutil.copy(self.h5p_input_file, self.h5p_test_file)
        # Get the path of the current file and create the path to the wiki2table.py script.
        cli = ['python3', self.exec_py, self.h5p_test_file, self.spreadsheet]
        for k,v in args.items():
            cli.append(k)
            if (v != ''):
                cli.append(v)
        proc = subprocess.run(cli, capture_output=True, text=True)
        return {
            'res': proc.returncode,
            'stdout': proc.stdout.strip().split('\n'),
            'stderr': proc.stderr.strip().split('\n')
        }

    def get_content_json(self, fname='content/content.json') -> dict:
        """Returns the whole object that is inside the content/content.json inside
        the given H5P package, or any other json file from the H5P package."""
        with zipfile.ZipFile(self.h5p_test_file) as zf:
            with zf.open(fname) as f:
                return json.load(f)
