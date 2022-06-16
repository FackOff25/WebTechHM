from urllib.parse import unquote_plus


def application(environ, start_response):

    body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
    parameter_pairs = body.split('&')
    parameter = dict()

    for parameter_pair in parameter_pairs:
        parameter_pair = parameter_pair.split('=')
        parameter[unquote_plus(parameter_pair[0])] = \
            unquote_plus(parameter_pair[1])

    output = repr(parameter)
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(output)))
    ]
    start_response(status, response_headers)
    return [output]
