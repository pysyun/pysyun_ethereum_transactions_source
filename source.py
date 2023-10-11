from web3 import Web3
from websockets import connect
import json
import asyncio
import requests
import time


class TransactionsSource:
    def __init__(self, ws_url, rpc, transaction_filter, database_url):
        self.ws_url = ws_url
        self.web3 = Web3(Web3.HTTPProvider(rpc))
        self.filter = transaction_filter
        self.database_url = database_url

    async def process(self):
        async with connect(self.ws_url) as ws:
            await ws.send(
                '{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}')
            subscription_response = await ws.recv()
            print(subscription_response)

            requests.post(self.database_url, json={
                "schema": "Ethereum Transactions Source"
            })

            while True:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=15)
                    response = json.loads(message)
                    if 'result' in response['params']:
                        tx_hash = response['params']['result']

                        tx_info = self.web3.eth.get_transaction(tx_hash)
                        if tx_info is not None:
                            if self.filter(tx_info):
                                requests.post(self.database_url, json={
                                    "schema": "Ethereum Transactions Source",
                                    "timeLine": tx_info['to']
                                })

                                database_response = requests.put(self.database_url, json={
                                    "time": int(time.time()),
                                    "value": str(tx_info)
                                }, params={
                                    'format': 'string',
                                    "schema": "Ethereum Transactions Source",
                                    "timeLine": tx_info['to']
                                })

                                if database_response.text != '1':
                                    print(f"Storage.Timeline error: {database_response.text}")
                except Exception as ex:
                    print(ex)
