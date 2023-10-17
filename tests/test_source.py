import asyncio
import unittest

from filters import contract_deployment
from source import TransactionsSource


class TestSource(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_initialize(self):

        source = TransactionsSource(
            "wss://dex.binance.org/api/ws",
            "https://bsc-dataseed.binance.org",
            contract_deployment)

        self.assertTrue(source is not None)

    def test_single_process(self):

        source = TransactionsSource(
            "wss://dex.binance.org/api/ws",
            "https://bsc-dataseed.binance.org",
            contract_deployment)

        async def process():
            data = source.process([])
            self.assertTrue(data == {})

        self.loop.run_until_complete(process())


if __name__ == '__main__':
    unittest.main()
