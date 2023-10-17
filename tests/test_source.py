import unittest

from filters import contract_deployment
from source import TransactionsSource


class TestSource(unittest.TestCase):

    def test_initialize(self):
        source = TransactionsSource(
            "wss://dex.binance.org/api/ws",
            "https://bsc-dataseed.binance.org",
            contract_deployment)

        self.assertTrue(source is not None)

    def test_process(self):
        source = TransactionsSource(
            "wss://dex.binance.org/api/ws",
            "https://bsc-dataseed.binance.org",
            contract_deployment)

        data = source.process()
        print(data)


if __name__ == '__main__':
    unittest.main()
