from setuptools import setup

setup(
    name='pysyun_ethereum_transactions_source',
    version='1.0',
    author='Illiatea',
    author_email='illiatea2@gmail.com',
    py_modules=['filters', 'source'],
    install_requires=['requests', 'web3', 'websockets']
)
