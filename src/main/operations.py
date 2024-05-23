from operation_amount import OperationAmount

class Operation:
    def __init__(self, id: int, state: str, date: str, operation_amount: OperationAmount, description: str, from_account: str, to_account: str):
        self.id = id
        self.state = state
        self.date = date
        self.operation_amount = operation_amount
        self.description = description
        self.from_account = from_account
        self.to_account = to_account

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(
            id=json_data.get('id'),
            state=json_data.get('state'),
            date=json_data.get('date'),
            operation_amount=OperationAmount.from_json(json_data.get('operationAmount', {})),
            description=json_data.get('description'),
            from_account=json_data.get('from'),
            to_account=json_data.get('to')
        )
