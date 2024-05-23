class OperationAmount:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency

    @classmethod
    def from_json(cls, json_data: dict):
        amount = json_data.get('amount')
        currency = json_data.get('currency', {}).get('name')
        return cls(
            amount=float(amount) if amount is not None else 0.0,
            currency=currency if currency is not None else "Unknown"
        )
