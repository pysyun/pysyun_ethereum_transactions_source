def contract_deployment(tx):
    return tx.get('to') is None


def payable_call(tx):
    return tx.get('to') is not None and tx.get('value') > 0
