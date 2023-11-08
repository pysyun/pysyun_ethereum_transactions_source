from web3 import Web3
from websockets import connect
import json
import asyncio
import time


class TransactionsSource:

    # TransactionsSource class constructor
    #
    # Args:
    #   ws_uri: Websocket URI to connect to for transaction events
    #   rpc_uri: JSON-RPC URI to query blockchain state
    #   transaction_filter: Function to filter transactions
    #
    #   TODO: For real-time polling, this should be replaced with a system with
    #    an intensive multi-threaded probabilistic polling. In real-time systems, the transaction call arguments
    #    should be available immediately from the transaction itself. Therefore, there is no purpose to get this data
    #    in a separate call.
    #   indexing_delay: Delay between receiving transaction hash and indexing transaction details
    #
    # The constructor initializes the websocket connection, JSON-RPC provider,
    # transaction filter function, and indexing delay.
    #
    # It also initializes empty dicts for transaction data and the background task.
    def __init__(self, ws_uri, rpc_uri, transaction_filter, indexing_delay=3):
        self.ws_url = ws_uri
        self.web3 = Web3(Web3.HTTPProvider(rpc_uri))
        self.filter = transaction_filter
        self.indexing_delay = indexing_delay
        self.data = {}
        self.task = None

    def process(self, _):

        # Create an execution loop task on the first run
        if self.task is None:
            self.task = asyncio.create_task(self.__process())

        result = self.data

        # Optionally, clean data not to cause buffering
        if not _:
            self.data = {}

        return result

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

                        await asyncio.sleep(self.indexing_delay)

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
