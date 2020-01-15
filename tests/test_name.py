import unittest

from elasticpypi.name import normalize, compute_version


class TestName(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(
            normalize("python-Levenshtein-0.12.0.tar.gz"), "python-levenshtein"
        )
        self.assertEqual(normalize("black-19.10b0-py36-none-any.whl"), "black")
        self.assertEqual(
            normalize("My-P_ac.kage-1.2.3dev-py36-none-any.whl"), "my-p-ac-kage"
        )

    def test_compute_version(self):
        self.assertEqual(compute_version("python-Levenshtein-0.12.0.tar.gz"), "0.12.0")
        self.assertEqual(compute_version("black-19.10b0-py36-none-any.whl"), "19.10b0")
        self.assertEqual(
            compute_version("My-P_ac.kage-1.2.3dev4-py36-none-any.whl"), "1.2.3dev4"
        )
