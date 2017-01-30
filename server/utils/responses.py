def error(error_message, status_code=400):
    assert(isinstance(error_message,str))
    return ({'error':error_message}, status_code, {'Content-Type':'application/json'})

def success(data_dict, status_code=200):
    assert(isinstance(data_dict,dict))
    return (data_dict, status_code, {'Content-Type':'application/json'})
