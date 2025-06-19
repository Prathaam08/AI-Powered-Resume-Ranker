import unittest
from app.utils import nlp_processor, scoring

class TestScoring(unittest.TestCase):
    def setUp(self):
        self.job_desc = "Looking for Python developer with 5+ years experience. Skills required: Python, Django, Flask, AWS. Machine learning knowledge is a plus."
        
    def test_scoring(self):
        resumes = [
            "Senior Python developer with 8 years experience. Expertise in Django, Flask, AWS. Machine learning background.",
            "Java developer with 3 years experience. Skills: Java, Spring, Hibernate.",
            "Python developer with 4 years experience. Proficient in Flask, Docker. Some AWS experience."
        ]
        
        # Mock resume data
        resume_data = [
            {'experience': 8, 'skills': {'python', 'django', 'flask', 'aws', 'machine learning'}},
            {'experience': 3, 'skills': {'java', 'spring', 'hibernate'}},
            {'experience': 4, 'skills': {'python', 'flask', 'docker', 'aws'}}
        ]
        
        preprocessed_job = nlp_processor.preprocess_text(self.job_desc)
        preprocessed_resumes = [nlp_processor.preprocess_text(r) for r in resumes]
        
        scores = scoring.calculate_scores(preprocessed_job, preprocessed_resumes, resume_data)
        
        self.assertEqual(len(scores), 3)
        self.assertGreater(scores[0], scores[1])  # Python dev should score higher than Java dev
        self.assertGreater(scores[0], scores[2])  # Senior should score higher than mid-level
        self.assertGreater(scores[2], scores[1])  # Python junior should score higher than Java dev
        
    def test_experience_extraction(self):
        text = "Software engineer with 5+ years of experience in web development."
        exp = nlp_processor.extract_experience(text)
        self.assertEqual(exp, 5)
        
        text = "Worked from Jan 2018 to Present"
        exp = nlp_processor.extract_experience(text)
        self.assertGreater(exp, 4)  # Should be about 5+ years

if __name__ == '__main__':
    unittest.main()