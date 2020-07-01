import json
from urllib.request import Request, urlopen


class Hasura:
    def __init__(self, address, secret):
        self.address = address
        self.secret = secret

    def query(self, string):
        request_body = '{"query":"' + string + '"}'
        data = str.encode(request_body)
        req = Request(self.address, data=data)
        req.add_header("X-Hasura-Admin-Secret", self.secret)
        content = urlopen(req)
        response = json.load(content)
        return response
