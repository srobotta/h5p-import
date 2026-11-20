#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
from test_base import TestBase

class TestExcel(TestBase):
    """Test all cli options of the import-cards.py script with the
    H5P Flash Card type and the Excel file."""

    def setUp(self) -> None:
        super().setUp()
        self.h5p_input_file = self.assets_dir + '/flashcards-1130.h5p'
        self.spreadsheet = self.assets_dir + '/words.xlsx'

    def test_without_args(self):
        """Test Excel sheet without any arguments."""

        data = self.run_command().get('stderr', [])
        self.assertEqual(data[0], "'7 x 3' -> '21'")
        self.assertEqual(data[3], "'9 x 13' -> '117'")
        self.assertEqual(data[5], '4 cards extracted.')
        self.assertEqual(data[6], f'Wrote 4 cards into {self.h5p_test_file}.')
        self.assertEqual(len(data), 7)
        h5p_content = self.get_content_json()
        self.assertEqual(4, len(h5p_content['cards']))
        self.assertEqual('70', h5p_content['cards'][2]['answer'])
        self.assertEqual('12 x 6', h5p_content['cards'][2]['text'])

    def test_row_and_sheet(self):
        """Test Excel sheet with argument row and sheet."""

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
        self.assertEqual(11, len(h5p_content['cards']))
        self.assertEqual('Wadenbein', h5p_content['cards'][10]['answer'])
        self.assertEqual('Calf bone', h5p_content['cards'][10]['text'])

    def test_row_sheet_cols(self):
        """Test Excel sheet with args row sheet front and back."""

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
        self.assertEqual(20, len(h5p_content['cards']))
        self.assertEqual('la tête', h5p_content['cards'][9]['answer'])
        self.assertEqual('Kopf', h5p_content['cards'][9]['text'])

    def test_title(self):
        """Test Excel sheet with the title argument, that fills the Flash Cards."""

        data = self.run_command({'--title': 'Custom title & "words" in a shell'}).get('stderr', [])
        self.assertEqual(data[0], "'7 x 3' -> '21'")
        self.assertEqual(data[6], f'Wrote 4 cards into {self.h5p_test_file}.')
        self.assertEqual(len(data), 7)
        h5p_content = self.get_content_json()
        self.assertEqual(4, len(h5p_content['cards']))
        self.assertEqual('625', h5p_content['cards'][1]['answer'])
        self.assertEqual('25 x 25', h5p_content['cards'][1]['text'])
        self.assertEqual('<p>Custom title &amp; &quot;words&quot; in a shell</p>', h5p_content['title'])
        h5p_content = self.get_content_json('h5p.json')
        self.assertEqual('Custom title & "words" in a shell', h5p_content['title'])

if __name__ == '__main__':
    unittest.main()