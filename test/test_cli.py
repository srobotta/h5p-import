#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
import subprocess
import os
import shutil
import tempfile
import uuid

class TestCli(unittest.TestCase):

    this_dir = os.path.dirname(os.path.realpath(__file__))
    assets_dir = f'{this_dir}/assets'
    temp_dir = tempfile.gettempdir()
    exec_py = f'{this_dir}/../import-cards.py'

    def setUp(self) -> None:
        return super().setUp()

    def runCommandAndGetResult(self, h5p, spreadsheet, args={}):
        # Get the path of the current file and create the path to the wiki2table.py script.
        cli = ['python3', self.exec_py, h5p, spreadsheet]
        for k,v in args.items():
            cli.append(k)
            if (v != ''):
                cli.append(v)
        result = subprocess.run(cli, capture_output=True, text=True)
        output = result.stdout.strip()
        return output

    def test_row_only(self):
        h5p_file = self.temp_dir + '/' + str(uuid.uuid4())[-12:] + '.h5p'
        shutil.copy(self.assets_dir + '/dialog-cards-1129.h5p', h5p_file)
        args = {
            '--row': '3',
        }
        out = self.runCommandAndGetResult(h5p_file, self.assets_dir + '/words.ods', args)
        data = out.split('\n')
        self.assertEqual(data[0], "'Bone (general)' -> 'Knochen (allgemein)'")
        self.assertEqual(data[10], "'Calf bone' -> 'Wadenbein'")
        self.assertEqual(len(data), 11)
        os.remove(h5p_file)

if __name__ == '__main__':
    unittest.main()