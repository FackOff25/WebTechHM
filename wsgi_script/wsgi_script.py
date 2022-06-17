from paste import request


def application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST' or environ['REQUEST_METHOD'] == 'GET':
        fields = request.parse_formvars(environ)
        data = make_byte_from_fields(fields)
        status = '200 OK'
    else:
        data = 'Not POST or GET'
        status = '404 Wrong Request'

    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)

    return iter([data])


def make_byte_from_fields(fields):
    to_return = ""
    for field in fields:
        to_return += 'Argument ' + field + ' is ' + fields[field] + '\n'

    return str.encode(to_return)

