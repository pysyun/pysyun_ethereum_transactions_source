def is_contract_deployment(tx):
    return tx.get('to') is None


def is_payable_call(tx):
    return tx.get('to') is not None and tx.get('value') > 0
