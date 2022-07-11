import json

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from backend.methods import handler as api_handler
import backend.jsonrpc as jsonrpc


class HomePageView(TemplateView):
    template_name = 'home.html'


@csrf_exempt
def api(request):
    request_id = None
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if jsonrpc.check(body):
            method = body.get('method')
            params = body.get('params')
            request_id = body.get('id')
            response = api_handler(method=method, params=params)
        else:
            response = dict(error='incorrect JSON-RPC 2.0 request')
    else:
        response = dict(
            error='incorrect http request, please use POST method'
        )

    rpc_response = jsonrpc.response(response, request_id)

    return JsonResponse(rpc_response, safe=False)

