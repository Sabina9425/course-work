from .utils import parse_operations
from datetime import datetime


def mask_card_number(card_number: str) -> str:
    if card_number and len(card_number) > 4:
        return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return card_number


def mask_account_number(account_number: str) -> str:
    if account_number and len(account_number) > 4:
        return f"**{account_number[-4:]}"
    return account_number


def print_last_executed_operations(json_file_path: str):
    operations = parse_operations(json_file_path)
    executed_operations = [op for op in operations if op.state == 'EXECUTED']
    executed_operations.sort(key=lambda x: x.date, reverse=True)

    for operation in executed_operations[:5]:
        date = datetime.strptime(operation.date, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        description = operation.description

        from_account = operation.from_account
        if from_account:
            from_account = mask_card_number(from_account) if " " in from_account else mask_account_number(from_account)

        to_account = operation.to_account
        if to_account:
            to_account = mask_account_number(to_account)

        amount = f"{operation.operation_amount.amount} {operation.operation_amount.currency}"

        print(f"{date} {description}")
        if from_account and to_account:
            print(f"{from_account} -> {to_account}")
        elif from_account:
            print(f"{from_account} -> Unknown")
        elif to_account:
            print(f"Unknown -> {to_account}")
        else:
            print("Unknown -> Unknown")
        print(f"{amount}")
        print("")
