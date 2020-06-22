
class DummyDataLoader:
    def __init__(table_name: str, data: dict):
        self.write(table_name, data)

    def write(table_name: str, data: dict):
        pass