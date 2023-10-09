# PySyun Timeline Ethereum Transactions Source

**Document Version**: 1.0.

**Author**: Syun Lee.

**Date**: 2023.10.09.

**Download whitepaper**: [pysyun_ethereum_transactions_source_whitepaper.pdf](./pysyun_ethereum_transactions_source_whitepaper.pdf)

## Project Introduction

The **PySyun Timeline Ethereum Transactions Source** is an innovative project aimed at providing a reliable and efficient solution for accessing and retrieving transaction data from an Ethereum node. With the growing popularity and adoption of blockchain technology, it has become increasingly important to have easy access to historical transaction information.

Our project focuses on leveraging the power of Python and the Syun library to streamline the process of retrieving transaction details from the Ethereum blockchain. By utilizing the Syun library's robust functionality and compatibility with Ethereum nodes, we have created a user-friendly and efficient tool for retrieving transaction timeline data.

## Key Features

1. **Ethereum Node Connectivity**: PySyun Timeline seamlessly connects to Ethereum nodes, offering real-time access to transaction data.
2. **Real-time Data Retrieval**: Our project allows users to retrieve transaction timelines from the Ethereum blockchain, enabling easy analysis and tracking of transaction activity.

By utilizing PySyun Timeline Ethereum Transactions Source, developers and blockchain enthusiasts can save valuable time and effort in accessing and analyzing transaction timelines from the Ethereum blockchain. Through its features and capabilities, our project aims to contribute to the advancement of blockchain technology and facilitate its widespread adoption in various industries.

## Filtering transactions
Type of transactions to be filtered can be specified with a lambda function,
which is passed as the constructor argument.

The "**filters.py**" module in the library contains such kind of filters.

### Filtering contract deployment transactions
Initially, the filter for a contract deployment transaction is available
in the "**filters.py**" module.
