import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from score import extract_dates, extract_numbers, score_response  # noqa: E402

DATE_Q = {"answer": "2 June 1943", "answer_type": "date", "distractors": ["1967"]}
NUMBER_Q = {"answer": "80", "answer_type": "number", "distractors": ["639"]}
TEXT_Q = {"answer": "Kennedy, Furner, Irvine-Smith and Joubert", "answer_type": "text",
          "accept": [], "distractors": ["Kallenbach, Kennedy and Furner"]}


class ExtractionTests(unittest.TestCase):
    def test_date_formats(self):
        for text in ["2 June 1943", "June 2, 1943", "2nd June 1943", "1943-06-02"]:
            self.assertIn((1943, 6, 2), extract_dates(text), text)

    def test_numbers_with_commas_and_currency(self):
        self.assertIn(3300.0, extract_numbers("It cost £3,300."))
        self.assertIn(1544.0, extract_numbers("provision for 1,544 beds"))


class ScoringTests(unittest.TestCase):
    def test_correct_date_in_other_format(self):
        self.assertEqual(score_response(DATE_Q, "He died on June 2, 1943.")["label"], "correct")

    def test_year_only_is_partial(self):
        self.assertEqual(score_response(DATE_Q, "He died in 1943.")["label"], "partial")

    def test_distractor(self):
        result = score_response(DATE_Q, "He passed away in 1967.")
        self.assertEqual(result["label"], "distractor")
        self.assertIn("mentions_distractor:1967", result["flags"])

    def test_abstention_beats_distractor(self):
        result = score_response(NUMBER_Q, "The opening figure is not specified; today it has 639 beds.")
        self.assertEqual(result["label"], "no_answer")
        self.assertIn("abstained", result["flags"])

    def test_text_answer_ignores_punctuation(self):
        self.assertEqual(score_response(TEXT_Q, "Kennedy Furner Irvine Smith & Joubert")["label"], "correct")

    def test_wrong(self):
        self.assertEqual(score_response(NUMBER_Q, "It opened with 120 beds.")["label"], "wrong")


if __name__ == "__main__":
    unittest.main()
