import unittest
from unittest.mock import patch, mock_open

# Assuming these functions and classes are defined in your code
from src.main.main import mask_card_number, mask_account_number, print_last_executed_operations
from src.main.operation_amount import OperationAmount, Currency
from src.main.operations import Operation
from src.main.utils import parse_operations

class TestMain(unittest.TestCase):

    def test_mask_card_number(self):
        self.assertEqual(mask_card_number("Visa 1234 5678 9012 3456"), "Visa 1234 56** **** 3456")
        self.assertEqual(mask_card_number("Visa Classic 6831982476737658"), "Visa Classic 6831 98** **** 7658")
        self.assertEqual(mask_card_number("1234"), "1234")
        self.assertEqual(mask_card_number(None), None)

    def test_mask_account_number(self):
        self.assertEqual(mask_account_number("счет 123456"), "счет **3456")
        self.assertEqual(mask_account_number("1234"), "1234")
        self.assertEqual(mask_account_number(None), None)

    def test_currency(self):
        currency = Currency(name="руб.", code="RUB")
        self.assertEqual(currency.name, "руб.")
        self.assertEqual(currency.code, "RUB")

    def test_operation_amount(self):
        currency = Currency(name="USD", code="USD")
        amount = OperationAmount(amount=12345.67, currency=currency)
        self.assertEqual(amount.amount, 12345.67)
        self.assertEqual(amount.currency.name, "USD")
        self.assertEqual(amount.currency.code, "USD")

    def test_operation(self):
        currency = Currency(name="USD", code="USD")
        amount = OperationAmount(amount=12345.67, currency=currency)
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
        self.assertEqual(operation.operation_amount.currency.name, "USD")
        self.assertEqual(operation.operation_amount.currency.code, "USD")
        self.assertEqual(operation.description, "Transfer")
        self.assertEqual(operation.from_account, "1234567890123456")
        self.assertEqual(operation.to_account, "654321")

    @patch("builtins.open", new_callable=mock_open, read_data="""
    [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": 1000.00, "currency": {"name": "USD", "code": "USD"}},
            "description": "Test",
            "from": "1234567890123456",
            "to": "654321"
        }
    ]
    """)
    def test_parse_operations(self, mock_file):
        operations = parse_operations("operations.json")
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0].id, 1)
        self.assertEqual(operations[0].state, "EXECUTED")
        self.assertEqual(operations[0].operation_amount.amount, 1000.00)
        self.assertEqual(operations[0].operation_amount.currency.name, "USD")
        self.assertEqual(operations[0].operation_amount.currency.code, "USD")
        self.assertEqual(operations[0].description, "Test")
        self.assertEqual(operations[0].from_account, "1234567890123456")
        self.assertEqual(operations[0].to_account, "654321")

    @patch('src.main.main.parse_operations')
    def test_print_last_executed_operations_no_operations(self, mock_parse_operations):
        mock_parse_operations.return_value = []

        expected_output = ""
        result = print_last_executed_operations("dummy_path")
        self.assertEqual(result, expected_output)

    @patch('src.main.main.parse_operations')
    def test_print_last_executed_operations_some_not_executed(self, mock_parse_operations):
        currency = Currency(name="USD", code="USD")
        operation_amount = OperationAmount(amount=12345.67, currency=currency)

        executed_operation = Operation(
            id=1,
            state="EXECUTED",
            date="2019-07-26T10:50:58.294041",
            operation_amount=operation_amount,
            description="Executed Transfer",
            from_account="visa 1234 5678 9012 3456",
            to_account="счет 654321"
        )

        not_executed_operation = Operation(
            id=2,
            state="PENDING",
            date="2019-08-26T10:50:58.294041",
            operation_amount=operation_amount,
            description="Pending Transfer",
            from_account="Visa Classic 1234567890123456",
            to_account="счет 654321"
        )

        mock_parse_operations.return_value = [executed_operation, not_executed_operation]

        expected_output = (
            "26.07.2019 Executed Transfer\n"
            "visa 1234 56** **** 3456 -> счет **4321\n"
            "12345.67 USD\n"
        )

        result = print_last_executed_operations("dummy_path")
        self.assertEqual(result, expected_output)

    @patch('src.main.main.parse_operations')
    def test_print_last_executed_operations_various_account_formats(self, mock_parse_operations):
        currency = Currency(name="USD", code="USD")
        operation_amount1 = OperationAmount(amount=12345.67, currency=currency)
        operation_amount2 = OperationAmount(amount=1000.00, currency=currency)

        operation1 = Operation(
            id=1,
            state="EXECUTED",
            date="2019-07-26T10:50:58.294041",
            operation_amount=operation_amount1,
            description="Transfer 1",
            from_account="Visa Gold 1234 5678 9012 3456",
            to_account="Счет 654321"
        )

        operation2 = Operation(
            id=2,
            state="EXECUTED",
            date="2019-08-26T10:50:58.294041",
            operation_amount=operation_amount2,
            description="Transfer 2",
            from_account="MasterCard 3152479541115065",
            to_account="Visa Gold 9447344650495960"
        )

        mock_parse_operations.return_value = [operation1, operation2]

        expected_output = (
            "26.08.2019 Transfer 2\n"
            "MasterCard 3152 47** **** 5065 -> Visa Gold 9447 34** **** 5960\n"
            "1000.0 USD\n\n"
            "26.07.2019 Transfer 1\n"
            "Visa Gold 1234 56** **** 3456 -> Счет **4321\n"
            "12345.67 USD\n"
        )

        result = print_last_executed_operations("dummy_path")
        self.assertEqual(result, expected_output)

    @patch('src.main.main.parse_operations')
    def test_print_last_executed_operations_more_than_five(self, mock_parse_operations):
        currency = Currency(name="USD", code="USD")
        operations = []

        for i in range(1, 7):
            operation_amount = OperationAmount(amount=1000.00 * i, currency=currency)
            operation = Operation(
                id=i,
                state="EXECUTED",
                date=f"2019-07-26T10:50:58.29404{i}",
                operation_amount=operation_amount,
                description=f"Transfer {i}",
                from_account=f"Visa 1234 5678 9012 345{i}",
                to_account="Счет 654321"
            )
            operations.append(operation)

        mock_parse_operations.return_value = operations

        expected_output = (
            "26.07.2019 Transfer 6\n"
            "Visa 1234 56** **** 3456 -> Счет **4321\n"
            "6000.0 USD\n\n"
            "26.07.2019 Transfer 5\n"
            "Visa 1234 56** **** 3455 -> Счет **4321\n"
            "5000.0 USD\n\n"
            "26.07.2019 Transfer 4\n"
            "Visa 1234 56** **** 3454 -> Счет **4321\n"
            "4000.0 USD\n\n"
            "26.07.2019 Transfer 3\n"
            "Visa 1234 56** **** 3453 -> Счет **4321\n"
            "3000.0 USD\n\n"
            "26.07.2019 Transfer 2\n"
            "Visa 1234 56** **** 3452 -> Счет **4321\n"
            "2000.0 USD\n"
        )

        result = print_last_executed_operations("dummy_path")
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()

