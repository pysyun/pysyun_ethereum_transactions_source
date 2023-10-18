import asyncio
import unittest

from filters import contract_deployment, each
from source import TransactionsSource


class TestSource(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_initialize(self):
        source = TransactionsSource(
            "wss://bsc.publicnode.com",
            "https://bsc-dataseed.binance.org",
            contract_deployment)
        self.assertTrue(source is not None)

    def test_single_process(self):
        source = TransactionsSource(
            "wss://bsc.publicnode.com",
            "https://bsc-dataseed.binance.org",
            contract_deployment)

        async def process():
            data = source.process([])
            self.assertTrue(data == {})

        self.loop.run_until_complete(process())

    def test_delayed_process(self):
        source = TransactionsSource(
            "wss://bsc.publicnode.com",
            "https://bsc-dataseed.binance.org",
            each)

        async def process():
            data = source.process([])
            print(data)

        async def delayed_process():
            for _ in range(17):
                await asyncio.sleep(1)
                await process()

        self.loop.run_until_complete(delayed_process())


if __name__ == '__main__':
    unittest.main()
