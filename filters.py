def contract_deployment(transaction):
    return transaction.get('to') is None


def payable_call(transaction):
    return transaction.get('to') is not None and transaction.get('value') > 0


def each(transaction):
    return True
