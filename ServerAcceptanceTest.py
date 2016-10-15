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
    port = 43287

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    @classmethod
    def setUpClass(self):
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

    @file_data('multiplechoicequestion_expressions.json')
    @unpack
    def test_multipleChoiceQuestion(self, question, correct, wrong, expression):
        t_url = Template("http://localhost:${port}/multiplechoicequestion?name=${question}&correct=${correct}&wrong=${wrong}")
        url = t_url.substitute(
            port=str(self.port),
            question=question,
            correct=','.join(map(lambda el: "'" + el + "'", correct)),
            wrong=','.join(map(lambda el: "'" + el + "'", wrong))
        )
        debug(url)
        reply = request.urlopen(url).read().decode()
        self.assertEqual(expression, reply)

    @classmethod
    def tearDownClass(self):
        self.httpd.shutdown()