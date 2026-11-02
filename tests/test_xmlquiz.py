# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
import importlib.util
from pathlib import Path
import sys
import unittest

spec = importlib.util.spec_from_file_location("xmlquiz", Path(__file__).resolve().parents[1] / "multiquestions-scrum-quiz-xml.py")
app = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = app
spec.loader.exec_module(app)

class XMLQuizTests(unittest.TestCase):
    def test_load(self):
        questions = app.load_questions()
        self.assertEqual(len(questions), 4)
        self.assertTrue(any(q.multi for q in questions))
    def test_full_score(self):
        questions = app.load_questions()
        answers = {i: set(q.correct) for i, q in enumerate(questions)}
        self.assertEqual(app.grade(questions, answers), (len(questions), len(questions)))
    def test_empty_score(self):
        questions = app.load_questions()
        self.assertEqual(app.grade(questions, {}), (0, len(questions)))

if __name__ == "__main__":
    unittest.main()
