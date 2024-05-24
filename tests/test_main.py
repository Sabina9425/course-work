import unittest
from main.main import mask_card_number, mask_account_number
from main.operation_amount import OperationAmount
from main.operations import Operation
from main.utils import parse_operations
from unittest.mock import patch, mock_open
import os

class TestMain(unittest.TestCase):

    def test_mask_card_number(self):
        self.assertEqual(mask_card_number("1234567890123456"), "1234 56** **** 3456")
        self.assertEqual(mask_card_number("1234"), "1234")
        self.assertEqual(mask_card_number(None), None)

    def test_mask_account_number(self):
        self.assertEqual(mask_account_number("12345678"), "**5678")
        self.assertEqual(mask_account_number("1234"), "1234")
        self.assertEqual(mask_account_number(None), None)

    def test_operation_amount(self):
        amount = OperationAmount(amount=12345.67, currency="USD")
        self.assertEqual(amount.amount, 12345.67)
        self.assertEqual(amount.currency, "USD")

    def test_operation(self):
        amount = OperationAmount(amount=12345.67, currency="USD")
        operation = Operation(
            id=1,
            state="EXECUTED",
            date="2019-07-26T10:50:58.294041",
            operation_amount=amount,
            description="Transfer",
            from_account="1234567890123456",
            to_account="654321"
        )
        self.assertEqual(operation.id, 1)
        self.assertEqual(operation.state, "EXECUTED")
        self.assertEqual(operation.date, "2019-07-26T10:50:58.294041")
        self.assertEqual(operation.operation_amount.amount, 12345.67)
        self.assertEqual(operation.operation_amount.currency, "USD")
        self.assertEqual(operation.description, "Transfer")
        self.assertEqual(operation.from_account, "1234567890123456")
        self.assertEqual(operation.to_account, "654321")

    def test_parse_operations(self):
        mock_json_data = """
        [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "1000.00", "currency": {"name": "USD"}},
                "description": "Test",
                "from": "1234567890123456",
                "to": "654321"
            }
        ]
        """
        with patch("builtins.open", mock_open(read_data=mock_json_data)):
            operations = parse_operations("operations.json")
            self.assertEqual(len(operations), 1)
            self.assertEqual(operations[0].id, 1)
            self.assertEqual(operations[0].state, "EXECUTED")
            self.assertEqual(operations[0].operation_amount.amount, 1000.00)
            self.assertEqual(operations[0].operation_amount.currency, "USD")
            self.assertEqual(operations[0].from_account, "1234567890123456")
            self.assertEqual(operations[0].to_account, "654321")

if __name__ == '__main__':
    unittest.main()

