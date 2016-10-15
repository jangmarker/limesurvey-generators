import unittest
from http.server import HTTPServer
from logging import debug
from string import Template
from threading import Thread
from typing import List
from urllib import request
from ddt import ddt, file_data, unpack

from server import GeneratorServer


@ddt
class ServerAcceptanceTest(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.port = 43287

    def setUp(self):
        self.httpd = HTTPServer(("", self.port), GeneratorServer)
        self.server_thread = Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    @file_data('orderquestion_expressions.json')
    @unpack
    def test_orderQuestion(self, question, ref: List[str], expression):
        t_url = Template("http://localhost:${port}/orderquestion?name=${question}&answer=${answer}")
        url = t_url.substitute(
            port=str(self.port),
            question=question,
            answer=','.join(map(lambda el: "'" + el + "'", ref))
        )
        debug(url)
        reply = request.urlopen(url).read().decode()
        self.assertEqual(expression, reply)

    def tearDown(self):
        self.httpd.shutdown()