def response(result, request_id):
    r = {'jsonrpc': '2.0', 'result': result}
    if request_id:
        r['id'] = request_id
    else:
        r['id'] = None
    return r


def check(body):
    # TODO: check request body for JSON-RPC 2.0 spec (https://www.jsonrpc.org/specification)
    return True
