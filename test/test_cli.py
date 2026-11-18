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

class TestCli(unittest.TestCase):

    this_dir = os.path.dirname(os.path.realpath(__file__))
    assets_dir = f'{this_dir}/assets'
    temp_dir = tempfile.gettempdir()
    exec_py = f'{this_dir}/../import-cards.py'

    def setUp(self) -> None:
        return super().setUp()

    def run_command(self, h5p_file, spreadsheet, args={}) -> dict:
        """Run the cli command "python3 import-cards.py" with the cli arguments
        and the two files passed to that function. The result contains the
        exit code, the output to stdout and stderr.
        """
        # Get the path of the current file and create the path to the wiki2table.py script.
        cli = ['python3', self.exec_py, h5p_file, spreadsheet]
        for k,v in args.items():
            cli.append(k)
            if (v != ''):
                cli.append(v)
        proc = subprocess.run(cli, capture_output=True, text=True)
        return {
            'res': proc.returncode,
            'stdout': proc.stdout.strip(),
            'strerr': proc.stderr.strip()
        }

    def get_content_json(self, h5p_file) -> dict:
        """Returns the whole object that is inside the content/content.json inside
        the given H5P package."""
        with zipfile.ZipFile(h5p_file) as zf:
            with zf.open('content/content.json') as f:
                return json.load(f)

    def test_row_only(self):
        h5p_file = self.temp_dir + '/' + str(uuid.uuid4())[-12:] + '.h5p'
        shutil.copy(self.assets_dir + '/dialog-cards-1129.h5p', h5p_file)
        args = {
            '--row': '3',
        }
        proc = self.run_command(h5p_file, self.assets_dir + '/words.ods', args)
        data = proc['strerr'].split('\n')
        self.assertEqual(data[0], "'Bone (general)' -> 'Knochen (allgemein)'")
        self.assertEqual(data[10], "'Calf bone' -> 'Wadenbein'")
        self.assertEqual(data[12], '11 cards extracted.')
        self.assertEqual(data[13], f'Wrote 11 cards into {h5p_file}.')
        self.assertEqual(len(data), 14)
        h5p_content = self.get_content_json(h5p_file)
        self.assertEqual(11, len(h5p_content['dialogs']))
        self.assertEqual('<p style="text-align:center;">Wadenbein</p>', h5p_content['dialogs'][10]['answer'])
        self.assertEqual('<p style="text-align:center;">Calf bone</p>', h5p_content['dialogs'][10]['text'])
        os.remove(h5p_file)

if __name__ == '__main__':
    unittest.main()