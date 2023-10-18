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
        self.task = None

    def process(self, _):

        # Create a task if not exists
        if self.task is None:
            self.task = asyncio.create_task(self.__process())

        return self.data

    def stop(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None

    async def __process(self):

        async with connect(self.ws_url) as ws:

            subscription = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "eth_subscribe",
                "params": ["newPendingTransactions"]
            }
            await ws.send(json.dumps(subscription))

            while True:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=15)
                    response = json.loads(message)

                    if 'params' in response and 'result' in response['params']:
                        tx_hash = response['params']['result']
                        transaction = self.web3.eth.get_transaction(tx_hash)

                        if transaction is not None and self.filter(transaction):
                            to_address = transaction['to']
                            current_time = int(time.time())

                            if to_address not in self.data:
                                self.data[to_address] = []

                            self.data[to_address].append({
                                "time": current_time,
                                "value": transaction
                            })
                except asyncio.TimeoutError:
                    pass
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"Error: {e}")
