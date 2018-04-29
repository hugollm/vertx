from .request import Request
from .response import Response
from .exceptions import BadLink, BadHandle


class Node(object):

    def __init__(self):
        self.nodes = []

    def __call__(self, env, start_response):
        request = Request(env)
        response = self.submit(request)
        return response.wsgi(start_response)

    def link(self, node):
        if not isinstance(node, Node):
            raise TypeError('A node can only link to node instances.')
        if node is self:
            raise BadLink('A node cannot link to itself.')
        self.nodes.append(node)
        self._validate_path(self)

    def _validate_path(self, start_node):
        for node in self.nodes:
            if node is start_node:
                raise BadLink('A node link must not form a path to itself.')
            node._validate_path(start_node)

    def submit(self, request, response=None):
        if response is None:
            response = Response()
        try:
            response = self.handle(request, response)
            bounce = False
        except Response as r:
            response = r
            bounce = True
        if not isinstance(response, Response):
            raise BadHandle('Node handle did not return or raise a response.')
        if not bounce:
            for node in self.nodes:
                response = node.submit(request, response)
        return response

    def handle(self, request, response):
        return response
