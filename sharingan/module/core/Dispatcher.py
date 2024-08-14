import json


class Dispatcher:
    def __init__(self, list_ingredients, encrypted_string, memory_block, memory_region, test_case):
        self.list_ingredients = list_ingredients
        self.encrypted_string = encrypted_string
        self.memory_block = memory_block
        self.memory_region = memory_region
        self.test_case = test_case

    def process(self):
        data = {
            'decryption_method': {
                'count': len(self.list_ingredients),
                'chain': self.list_ingredients
            },
            'encrypted_string': self.encrypted_string,
            'memory_block': self.memory_block,
            'memory_region': self.memory_region,
            'test_case': self.test_case
        }
        json_string = json.dumps(data, default = lambda x: x.__dict__)
        print(json_string)

    def test_sample(self) -> str:
        print('Test Sample')
        return 'Decrypted string'


