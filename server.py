from ast import literal_eval
from http.server import BaseHTTPRequestHandler, HTTPServer
from logging import fatal
from urllib.parse import parse_qs, urlparse

from OrderQuestionGenerator import expression


class GeneratorServer(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/orderquestion':
            query = parse_qs(url.query)
            question_name = query['name']
            reference = literal_eval('[' + query['answer'][0] + ']')

            output = expression(question_name, reference)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(output.encode())

httpd = HTTPServer(("", 80), GeneratorServer)
httpd.serve_forever()