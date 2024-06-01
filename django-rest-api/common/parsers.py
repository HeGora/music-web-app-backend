from rest_framework import parsers
from django.http import QueryDict
import json

class MultipartJSONParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = json.loads(result.data["data"])
        qdict = QueryDict('', mutable=True)
        qdict.update(data)
        print(data)
        print(qdict)
        return parsers.DataAndFiles(qdict, result.files)