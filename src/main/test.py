from utils import parse_operations

json_file_path = 'operations.json'
operations_list = parse_operations(json_file_path)

for operation in operations_list:
    print(operation.__dict__)
