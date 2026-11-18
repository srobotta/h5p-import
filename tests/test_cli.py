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
            'stderr': proc.stderr.strip()
        }

    def get_content_json(self, h5p_file, ftype='content/content.json') -> dict:
        """Returns the whole object that is inside the content/content.json inside
        the given H5P package, or any other json file from the H5P package."""
        with zipfile.ZipFile(h5p_file) as zf:
            with zf.open(ftype) as f:
                return json.load(f)

    def test_without_args(self):
        """Test simple without any arguments. That takes the rows A and B from
        the first sheet."""

        h5p_file = self.temp_dir + '/' + str(uuid.uuid4())[-12:] + '.h5p'
        shutil.copy(self.assets_dir + '/dialog-cards-1129.h5p', h5p_file)
        proc = self.run_command(h5p_file, self.assets_dir + '/words.ods')
        data = proc['stderr'].split('\n')
        self.assertEqual(data[0], "'7 x 3' -> '21'")
        self.assertEqual(data[3], "'9 x 13' -> '117'")
        self.assertEqual(data[5], '4 cards extracted.')
        self.assertEqual(data[6], f'Wrote 4 cards into {h5p_file}.')
        self.assertEqual(len(data), 7)
        h5p_content = self.get_content_json(h5p_file)
        self.assertEqual(4, len(h5p_content['dialogs']))
        self.assertEqual('<p style="text-align:center;">70</p>', h5p_content['dialogs'][2]['answer'])
        self.assertEqual('<p style="text-align:center;">12 x 6</p>', h5p_content['dialogs'][2]['text'])
        os.remove(h5p_file)

    def test_row_and_sheet(self):
        """Test with argument row and sheet to extract the body parts in English
        and German from the second sheet, skipping the header rows."""
        h5p_file = self.temp_dir + '/' + str(uuid.uuid4())[-12:] + '.h5p'
        shutil.copy(self.assets_dir + '/dialog-cards-1129.h5p', h5p_file)
        args = {
            '--row': '3',
            '--sheet': 'Knochen'
        }
        proc = self.run_command(h5p_file, self.assets_dir + '/words.ods', args)
        data = proc['stderr'].split('\n')
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

    def test_row_sheet_cols(self):
        """Test also with row and column argument to extract a wordlist sonmewhere in the middle
        of a worksheet."""

        h5p_file = self.temp_dir + '/' + str(uuid.uuid4())[-12:] + '.h5p'
        shutil.copy(self.assets_dir + '/dialog-cards-1129.h5p', h5p_file)
        args = {
            '--row': '4',
            '--sheet': 'FR Vocabulary',
            '--front': 'D',
            '--back': 'E',
        }
        proc = self.run_command(h5p_file, self.assets_dir + '/words.ods', args)
        data = proc['stderr'].split('\n')
        self.assertEqual(data[0], "'Mann' -> 'l’homme (m)'")
        self.assertEqual(data[19], "'Haut' -> 'la peau'")
        self.assertEqual(data[21], '20 cards extracted.')
        self.assertEqual(data[22], f'Wrote 20 cards into {h5p_file}.')
        self.assertEqual(len(data), 23)
        h5p_content = self.get_content_json(h5p_file)
        self.assertEqual(20, len(h5p_content['dialogs']))
        self.assertEqual('<p style="text-align:center;">la tête</p>', h5p_content['dialogs'][9]['answer'])
        self.assertEqual('<p style="text-align:center;">Kopf</p>', h5p_content['dialogs'][9]['text'])
        os.remove(h5p_file)

    def test_title(self):
        """Test with the title argument, that fills the respective properties in the content.json
        as well as in the h5p.json."""

        h5p_file = self.temp_dir + '/' + str(uuid.uuid4())[-12:] + '.h5p'
        shutil.copy(self.assets_dir + '/dialog-cards-1129.h5p', h5p_file)
        args = {
            '--title': 'Custom title & "words" in a shell',
        }
        proc = self.run_command(h5p_file, self.assets_dir + '/words.ods', args)
        data = proc['stderr'].split('\n')
        self.assertEqual(data[0], "'7 x 3' -> '21'")
        self.assertEqual(data[6], f'Wrote 4 cards into {h5p_file}.')
        self.assertEqual(len(data), 7)
        h5p_content = self.get_content_json(h5p_file)
        self.assertEqual(4, len(h5p_content['dialogs']))
        self.assertEqual('<p style="text-align:center;">625</p>', h5p_content['dialogs'][1]['answer'])
        self.assertEqual('<p style="text-align:center;">25 x 25</p>', h5p_content['dialogs'][1]['text'])
        self.assertEqual('<p>Custom title &amp; &quot;words&quot; in a shell</p>', h5p_content['title'])
        h5p_content = self.get_content_json(h5p_file, 'h5p.json')
        self.assertEqual('Custom title & "words" in a shell', h5p_content['title'])
        os.remove(h5p_file)

if __name__ == '__main__':
    unittest.main()