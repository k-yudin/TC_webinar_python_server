import http.server
import json
import urllib.parse
import re


class Handler(http.server.BaseHTTPRequestHandler):
    error_message_format = ""

    def _send_common_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    # noinspection PyPep8Naming
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path != "/api/hello":
            self.send_error(404, "")
            return

        self._send_common_headers()
        request_params = urllib.parse.parse_qs(parsed_url.query)
        has_name = re.match("(^|&)name=", parsed_url.query)

        name_list = request_params.get('name')
        if has_name and name_list is None:
            self.send_error_response("Bad name")
            return

        if name_list is None:
            self.send_answer_response("Hello, someeeone")
            return

        name = name_list.pop()

        # TODO
        # this doesn't work with russian symbols actually
        # but I can't understand what's wrong
        if not re.match('^[А-Яа-яA-Za-z]+$', name):
            self.send_error_response("Bad name")
            return

        self.send_answer_response("Hello, {name}".format(name=name))

    def send_answer_response(self, answer):
        self.wfile.write(json.dumps({'answer': answer}).encode('utf-8'))
        pass

    def send_error_response(self, error):
        self.wfile.write(json.dumps({'error': error}).encode('utf-8'))
        pass


if __name__ == '__main__':
    print("starting")
    httpd = http.server.HTTPServer(('0.0.0.0', 80), Handler)
    httpd.serve_forever()
