import unittest

from elasticpypi.name import normalize_name, normalize_version, get_parts


class TestName(unittest.TestCase):
    def test_get_parts(self):
        self.assertEqual(
            get_parts("python-Levenshtein-0.12.0.tar.gz"),
            ("python-levenshtein", "0.12.0"),
        )
        self.assertEqual(
            get_parts("black-19.10b0-py36-none-any.whl"), ("black", "19.10b0")
        )
        self.assertEqual(
            get_parts("repo_checker-5.7.0.dev33875-py3-none-any.whl"),
            ("repo-checker", "5.7.0.dev33875"),
        )
        self.assertEqual(
            get_parts("My-P_ac.kage-1.2.3dev2-py36-none-any.whl"),
            ("my-p-ac-kage", "1.2.3.dev2"),
        )
        self.assertEqual(
            get_parts("unknown-py36-none-any.WHL"), ("unknown-py36-none-any", "0.0.0"),
        )
        self.assertEqual(
            get_parts("unknown-py36-none-any"), ("unknown-py36-none-any", "0.0.0"),
        )

    def test_normalize_name(self):
        self.assertEqual(
            normalize_name("python-Levenshtein-0.12.0.tar.gz"), "python-levenshtein"
        )
        self.assertEqual(normalize_name("black-19.10b0-py36-none-any.whl"), "black")
        self.assertEqual(
            normalize_name("My-P_ac.kage-1.2.3dev-py36-none-any.whl"), "my-p-ac-kage"
        )

    def test_normalize_version(self):
        self.assertEqual(
            normalize_version("python-Levenshtein-0.12.0.tar.gz"), "0.12.0"
        )
        self.assertEqual(
            normalize_version("black-19.10b0-py36-none-any.whl"), "19.10b0"
        )
        self.assertEqual(
            normalize_version("My-P_ac.kage-1.2.3.dev4-py36-none-any.whl"), "1.2.3.dev4"
        )
        self.assertEqual(
            normalize_version("My-P_ac.kage-1.2.3.rc4-py36-none-any.whl"), "1.2.3rc4"
        )
