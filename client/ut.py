import unittest

from bs1 import R, check_ticker


class Test_check_ticker(unittest.TestCase):

    def test_check_ticker(self):

        ticker = ''
        result = check_ticker(ticker)
        self.assertEqual(R.ERROR1, result)

        ticker = '_%'
        result = check_ticker(ticker)
        self.assertEqual(R.ERROR2, result)

        ticker = 'a'
        result = check_ticker(ticker)
        self.assertEqual(ticker, result)

        ticker = 'a_'
        result = check_ticker(ticker)
        self.assertEqual(ticker, result)

        ticker = '_'
        result = check_ticker(ticker)
        self.assertEqual(R.ERROR2, result)

        ticker = 'a&b'
        result = check_ticker(ticker)
        self.assertEqual(R.ERROR2, result)


if __name__ == "__main__":
    unittest.main()
