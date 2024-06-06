from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.parsers import QueryDict, DataAndFiles
from unittest.mock import MagicMock
from common.parsers import MultipartJSONParser
import json
import io
import unittest

#refactor using data-factory library
class MultipartJSONParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = MultipartJSONParser()
        self.stream = io.BytesIO(b'')
        self.media_type = "multipart/form-data; boundary=boundary"
        self.parser_context = {"request": MagicMock()}

    def test_parse(self):
        data = {
            "data": json.dumps({"name": "John", "age": 30}),
            "file": SimpleUploadedFile("file.txt", b"file_content")
        }
        files = {"file": data["file"]}
        content = f"--boundary\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n{data['data']}\r\n--boundary\r\nContent-Disposition: form-data; name=\"file\"; filename=\"file.txt\"\r\nContent-Type: text/plain\r\n\r\nfile_content\r\n--boundary--"
        self.stream = io.BytesIO(content.encode())
        
        result = self.parser.parse(self.stream, media_type=self.media_type, parser_context=self.parser_context)
        
        expected_data = QueryDict(mutable=True)
        expected_data.update({"name": "John", "age": "30"})
        self.assertEqual(result.data, expected_data)
        self.assertEqual(result.files, files)