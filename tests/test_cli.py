#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
from test_base import TestBase

class TestCli(TestBase):
    """Test all cli options of the import-cards.py script with the
    H5P Dialog Card type and the ODS file."""

    def setUp(self) -> None:
        super().setUp()
        self.h5p_input_file = self.assets_dir + '/dialog-cards-1129.h5p'
        self.spreadsheet = self.assets_dir + '/words.ods'

    def test_without_args(self):
        """Test ODS without any arguments."""

        data = self.run_command().get('stderr', [])
        self.assertEqual(data[0], "'7 x 3' -> '21'")
        self.assertEqual(data[3], "'9 x 13' -> '117'")
        self.assertEqual(data[5], '4 cards extracted.')
        self.assertEqual(data[6], f'Wrote 4 cards into {self.h5p_test_file}.')
        self.assertEqual(len(data), 7)
        h5p_content = self.get_content_json()
        self.assertEqual(4, len(h5p_content['dialogs']))
        self.assertEqual('<p style="text-align:center;">70</p>', h5p_content['dialogs'][2]['answer'])
        self.assertEqual('<p style="text-align:center;">12 x 6</p>', h5p_content['dialogs'][2]['text'])

    def test_row_and_sheet(self):
        """Test ODS with argument row and sheet."""

        data = self.run_command({
            '--row': '3',
            '--sheet': 'Knochen'
        }).get('stderr', [])
        self.assertEqual(data[0], "'Bone (general)' -> 'Knochen (allgemein)'")
        self.assertEqual(data[10], "'Calf bone' -> 'Wadenbein'")
        self.assertEqual(data[12], '11 cards extracted.')
        self.assertEqual(data[13], f'Wrote 11 cards into {self.h5p_test_file}.')
        self.assertEqual(len(data), 14)
        h5p_content = self.get_content_json()
        self.assertEqual(11, len(h5p_content['dialogs']))
        self.assertEqual('<p style="text-align:center;">Wadenbein</p>', h5p_content['dialogs'][10]['answer'])
        self.assertEqual('<p style="text-align:center;">Calf bone</p>', h5p_content['dialogs'][10]['text'])

    def test_row_sheet_cols(self):
        """Test ODS with arguments row, sheet, front and back."""

        data = self.run_command({
            '--row': '4',
            '--sheet': 'FR Vocabulary',
            '--front': 'D',
            '--back': 'E',
        }).get('stderr', [])
        self.assertEqual(data[0], "'Mann' -> 'l’homme (m)'")
        self.assertEqual(data[19], "'Haut' -> 'la peau'")
        self.assertEqual(data[21], '20 cards extracted.')
        self.assertEqual(data[22], f'Wrote 20 cards into {self.h5p_test_file}.')
        self.assertEqual(len(data), 23)
        h5p_content = self.get_content_json()
        self.assertEqual(20, len(h5p_content['dialogs']))
        self.assertEqual('<p style="text-align:center;">la tête</p>', h5p_content['dialogs'][9]['answer'])
        self.assertEqual('<p style="text-align:center;">Kopf</p>', h5p_content['dialogs'][9]['text'])

    def test_title(self):
        """Test ODS with the title argument, verify Dialog Card."""

        data = self.run_command({'--title': 'Custom title & "words" in a shell'}).get('stderr', [])
        self.assertEqual(data[0], "'7 x 3' -> '21'")
        self.assertEqual(data[6], f'Wrote 4 cards into {self.h5p_test_file}.')
        self.assertEqual(len(data), 7)
        h5p_content = self.get_content_json()
        self.assertEqual(4, len(h5p_content['dialogs']))
        self.assertEqual('<p style="text-align:center;">625</p>', h5p_content['dialogs'][1]['answer'])
        self.assertEqual('<p style="text-align:center;">25 x 25</p>', h5p_content['dialogs'][1]['text'])
        self.assertEqual('<p>Custom title &amp; &quot;words&quot; in a shell</p>', h5p_content['title'])
        h5p_content = self.get_content_json('h5p.json')
        self.assertEqual('Custom title & "words" in a shell', h5p_content['title'])

if __name__ == '__main__':
    unittest.main()