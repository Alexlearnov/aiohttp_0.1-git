from aiohttp.web_response import json_response

def index(request):
    return json_response(data={"data": "Hello its my first start"})