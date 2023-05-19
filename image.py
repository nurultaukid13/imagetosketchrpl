class Image:
    def __init__(self, file_path: str, weight: int, format: str):
        self.file_path = file_path
        self.weight = weight
        self.format = format

    def get_file_path(self) -> str:
        return self.file_path

    def get_weight(self) -> int:
        return self.weight

    def get_format(self) -> str:
        return self.format