import unittest
from services.exam_service import create_exam, get_exams

class TestExam(unittest.TestCase):

    def test_create_exam(self):
        create_exam("Test Exam")
        exams = get_exams()
        self.assertTrue(len(exams) > 0)

if __name__ == '__main__':
    unittest.main()