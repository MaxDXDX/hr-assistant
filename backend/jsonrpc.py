def response(result, request_id):
    r = {'jsonrpc': '2.0'}
    r['result'] = result
    r['id'] = request_id
    return r
