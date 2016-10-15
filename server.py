from ast import literal_eval
from http.server import BaseHTTPRequestHandler, HTTPServer
from logging import fatal
from urllib.parse import parse_qs, urlparse

import MultipleChoiceQuestionGenerator
import OrderQuestionGenerator


def extract_array(query, key):
    return literal_eval('[' + query[key][0] + ']')


class GeneratorServer(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        question_name = query['name'][0]
        if url.path == '/orderquestion':
            reference = extract_array(query, 'answer')
            output = OrderQuestionGenerator.expression(question_name, reference)
            status = 200
        elif url.path == '/multiplechoicequestion':
            correct = extract_array(query, 'correct')
            wrong = extract_array(query, 'wrong')
            output = MultipleChoiceQuestionGenerator.generate(question_name, correct, wrong)
            status = 200
        else:
            output = "route does not exist"
            status = 404

        self.send_response(status)
        self.end_headers()
        self.wfile.write(output.encode())

if __name__ == '__main__':
    httpd = HTTPServer(("", 42387), GeneratorServer)
    httpd.serve_forever()