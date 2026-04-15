def to_jsonrpc(method, params, request_id=1):
    return {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id
    }

data = {"a": 5, "b": 7}
rpc = to_jsonrpc("add_numbers", data)
print(rpc)