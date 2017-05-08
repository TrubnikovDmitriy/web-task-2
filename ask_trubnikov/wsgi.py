from cgi import parse_qsl


def get_post_8002(environ, start_response):

    S = parse_qsl(environ["QUERY_STRING"])
    if (environ["REQUEST_METHOD"] == "GET"):
        output = ["<h3>Get:</h3>"]
        for pair in S:
            output.append('</b> = '.join(pair))
            output.append('<br>')
    else:
        if (environ["REQUEST_METHOD"] == "POST"):
            output = ["<h3>Post:</h3>"]

        else:
            output = ["<h3>Another request</h3>"]
    output.append('(8002)')
    start_response('200 OK', [('Content-type', 'text/html')])
    return output


def get_post_8001(environ, start_response):

    S = parse_qsl(environ["QUERY_STRING"])
    if (environ["REQUEST_METHOD"] == "GET"):
        output = ["<h3>Get:</h3>"]
        for pair in S:
            output.append('</b> = '.join(pair))
            output.append('<br>')
    else:
        if (environ["REQUEST_METHOD"] == "POST"):
            output = ["<h3>Post:</h3>"]

        else:
            output = ["<h3>Another request</h3>"]
    output.append('(8001)')
    start_response('200 OK', [('Content-type', 'text/html')])
    return output


def hello_world(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    return("Hello, World")
