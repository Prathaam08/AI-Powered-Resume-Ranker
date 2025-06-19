import unittest
import os
from app.utils import file_parser

class TestFileParser(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.sample_pdf = os.path.join(self.test_dir, '..', 'data', 'resumes', 'sample.pdf')
        self.sample_docx = os.path.join(self.test_dir, '..', 'data', 'resumes', 'sample.docx')
        self.sample_txt = os.path.join(self.test_dir, '..', 'data', 'resumes', 'sample.txt')
        
    def test_pdf_parsing(self):
        text = file_parser.extract_text(self.sample_pdf)
        self.assertGreater(len(text), 100)
        self.assertIn("Experience", text)
        
    def test_docx_parsing(self):
        text = file_parser.extract_text(self.sample_docx)
        self.assertGreater(len(text), 100)
        self.assertIn("Education", text)
        
    def test_txt_parsing(self):
        text = file_parser.extract_text(self.sample_txt)
        self.assertGreater(len(text), 100)
        self.assertIn("Skills", text)
        
    def test_contact_extraction(self):
        text = "Contact me at john.doe@example.com or 123-456-7890"
        contact = file_parser.extract_contact_info(text)
        self.assertEqual(contact['email'], 'john.doe@example.com')
        self.assertEqual(contact['phone'], '123-456-7890')

if __name__ == '__main__':
    unittest.main()