from src.main.utils import parse_operations
from datetime import datetime
import re

def mask_card_number(card_number: str) -> str:
    if not card_number:
        return card_number

    pattern = re.compile(r'(\d{4})\s?(\d{4})\s?(\d{4})\s?(\d{4})')
    def mask(match):
        groups = match.groups()
        return f"{groups[0]} {groups[1][:2]}** **** {groups[3]}"

    masked_card_number = pattern.sub(mask, card_number)

    return masked_card_number

def mask_account_number(account_number: str) -> str:
    if not account_number:
        return account_number

    parts = account_number.split()
    for i, part in enumerate(parts):
        if part.isdigit() and len(part) > 4:
            parts[i] = f"**{part[-4:]}"
    return ' '.join(parts)

def print_last_executed_operations(json_file_path: str) -> str:
    operations = parse_operations(json_file_path)
    executed_operations = [op for op in operations if op.state == 'EXECUTED']
    executed_operations.sort(key=lambda x: x.date, reverse=True)

    result = []

    for operation in executed_operations[:5]:
        date = datetime.strptime(operation.date, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        description = operation.description

        from_account = operation.from_account
        if from_account:
            if "счет" in from_account.lower():
                from_account = mask_account_number(from_account)
            else:
                from_account = mask_card_number(from_account)

        to_account = operation.to_account
        if to_account:
            if "счет" in to_account.lower():
                to_account = mask_account_number(to_account)
            else:
                to_account = mask_card_number(to_account)

        amount = f"{operation.operation_amount.amount} {operation.operation_amount.currency.name}"

        result.append(f"{date} {description}")
        if from_account and to_account:
            result.append(f"{from_account} -> {to_account}")
        elif from_account:
            result.append(f"{from_account} -> Unknown")
        elif to_account:
            result.append(f"Unknown -> {to_account}")
        else:
            result.append("Unknown -> Unknown")
        result.append(f"{amount}")
        result.append("")

    return "\n".join(result)

if __name__ == '__main__':
    print(print_last_executed_operations("operations.json"))
