class Currency:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

    @classmethod
    def from_json(cls, json_data: dict):
        name = json_data.get('name')
        code = json_data.get('code')
        return cls(
            name=name if name is not None else "Unknown",
            code=code if code is not None else "Unknown"
        )

class OperationAmount:
    def __init__(self, amount: float, currency: Currency):
        self.amount = amount
        self.currency = currency

    @classmethod
    def from_json(cls, json_data: dict):
        amount = json_data.get('amount')
        currency_data = json_data.get('currency', {})
        currency = Currency.from_json(currency_data)
        return cls(
            amount=float(amount) if amount is not None else 0.0,
            currency=currency
        )
