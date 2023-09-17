from aiohttp import FormData


class InputFile:
    def __init__(self, file_type: str, filename: str):
        self.data = FormData()
        self.file = open(filename, 'rb')
        self.data.add_field(file_type, value=self.file, filename=filename, content_type='multipart/form-data')