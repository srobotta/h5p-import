#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import unittest
from test_base import TestBase

class TestFillTheBlanks(TestBase):
    """Test the QuestionSet (Fill the blanks) with the Excel file."""

    def setUp(self) -> None:
            super().setUp()
            self.h5p_input_file = self.assets_dir + '/question-set-1128.h5p'
            self.spreadsheet = self.assets_dir + '/words.xlsx'
    
    def test_without_args(self):
        """Test QuestionSet without any arguments."""

        data = self.run_command().get('stderr', [])
        self.assertEqual(data[0], "'7 x 3' -> '21'")
        self.assertEqual(data[3], "'9 x 13' -> '117'")
        self.assertEqual(data[5], '4 cards extracted.')
        self.assertEqual(data[6], f'Wrote 4 cards into {self.h5p_test_file}.')
        self.assertEqual(len(data), 7)
        h5p_content = self.get_content_json()
        self.assertEqual(4, len(h5p_content['questions']))
        self.assertEqual('7 x 3', h5p_content['questions'][0]['metadata']['title'])
        self.assertEqual('<p>7 x 3: *21*</p>', h5p_content['questions'][0]['params']['questions'][0])
        self.assertEqual('Fill in the missing words', h5p_content['questions'][0]['params']['text'])
        self.assertRegex(h5p_content['questions'][0]['subContentId'], r'^[a-f0-9]{8}\-([a-f0-9]{4}\-){3}[a-f0-9]{12}$')
        # Check that the subContentIds are unique.
        unique_keys = {item['subContentId'] for item in h5p_content['questions']}
        self.assertEqual(4, len(unique_keys))

    def test_row_sheet_cols(self):
        """Test QuestionSet with flipped columns C -> B."""

        self.run_command({
            '--row': '3',
            '--sheet': 'Knochen',
            '--front': 'C',
            '--back': 'B',
        })
        h5p_content = self.get_content_json()
        self.assertEqual(11, len(h5p_content['questions']))
        self.assertEqual('Clavicula', h5p_content['questions'][2]['metadata']['title'])
        self.assertEqual('<p>Clavicula: *Schlüsselbein*</p>', h5p_content['questions'][2]['params']['questions'][0])

    def test_title(self):
        """Test QuestionSet with the title argument."""

        data = self.run_command({'--title': 'Custom title & "words" in a shell'}).get('stderr', [])
        self.assertEqual(data[0], "'7 x 3' -> '21'")
        self.assertEqual(data[6], f'Wrote 4 cards into {self.h5p_test_file}.')
        self.assertEqual(len(data), 7)
        h5p_content = self.get_content_json()
        self.assertEqual(4, len(h5p_content['questions']))
        self.assertEqual('9 x 13', h5p_content['questions'][3]['metadata']['title'])
        self.assertEqual('<p>9 x 13: *117*</p>', h5p_content['questions'][3]['params']['questions'][0])
        self.assertEqual('<p>Custom title &amp; &quot;words&quot; in a shell</p>', h5p_content['questions'][3]['params']['text'])
        h5p_content = self.get_content_json('h5p.json')
        self.assertEqual('Custom title & "words" in a shell', h5p_content['title'])

if __name__ == '__main__':
    unittest.main()
