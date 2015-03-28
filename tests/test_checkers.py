import testtools

import bashlint


class TestCheckers(testtools.TestCase):

    def _check_ok(self, checker, cases):
        for case in cases:
            self.assertIsNone(checker(case))

    def _check_error(self, checker, cases):
        for case, offset in cases:
            result = checker(case)
            self.assertIsNotNone(result)
            self.assertEqual(result[0], offset, "\nTestcase: '%s'\n" % case)

    def test_w201_ok(self):
        self._check_ok(bashlint.checker_trailing_whitespace, [
            "\n",
            "\r",
            "echo Test",
            "echo Test\n",
            "echo Test\r",
        ])

    def test_w201_error(self):
        self._check_error(bashlint.checker_trailing_whitespace, [
            ("\n ", 1),
            (" \n", 0),
            ("echo Test ", 9),
            ("echo Test\n ", 10),
            ("echo Test \n", 9),
            ("echo Test \n ", 11),
        ])

    def test_w202_ok(self):
        self._check_ok(bashlint.checker_trailing_whitespace, [
            "",
        ])

    def test_w202_error(self):
        self._check_error(bashlint.checker_trailing_whitespace, [
            (" ", 0),
            ("    ", 0),
        ])

    def test_w203_ok(self):
        self._check_ok(bashlint.checker_trailing_semicolon, [
            "",
            "echo Test",
            "echo Test; echo Test2",
            " ;; ",
            "find -type f -exec cat {} \;",
        ])

    def test_w203_error(self):
        self._check_error(bashlint.checker_trailing_semicolon, [
            (";", 0),
            ("    ;", 4),
            ("echo Test;", 9),
            ("echo Test;  ", 9),
            ("echo Test; echo Test2;", 21),
        ])
