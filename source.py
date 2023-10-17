from web3 import Web3
from websockets import connect
import json
import asyncio
import time


class TransactionsSource:
    def __init__(self, ws_url, rpc, transaction_filter):
        self.ws_url = ws_url
        self.web3 = Web3(Web3.HTTPProvider(rpc))
        self.filter = transaction_filter
        self.data = {}
        self.process_task = None

    def process(self):
        if self.process_task is None:
            self.process_task = asyncio.create_task(self.__process())

        else:
            return [self.data]

    async def __process(self):
        async with connect(self.ws_url) as ws:
            await ws.send(
                '{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}')
            subscription_response = await ws.recv()
            print(subscription_response)

            while True:
                message = await asyncio.wait_for(ws.recv(), timeout=15)
                response = json.loads(message)
                if 'result' in response['params']:
                    tx_hash = response['params']['result']

                    tx_info = self.web3.eth.get_transaction(tx_hash)
                    if tx_info is not None:
                        if self.filter(tx_info):
                            to_address = tx_info['to']
                            current_time = int(time.time())

                            if to_address not in self.data:
                                self.data[to_address] = []

                            self.data[to_address].append({
                                "time": current_time,
                                "value": tx_info
                            })
