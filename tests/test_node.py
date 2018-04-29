from unittest import TestCase
from unittest.mock import Mock

from vertx import Node, Request, Response
from vertx.exceptions import BadLink, BadHandle


class WsgiTestCase(TestCase):

    def test_node_is_a_wsgi_app(self):
        node = Node()
        start_response = Mock()
        body = node({}, start_response)
        start_response.assert_called_with('404 Not Found', [])
        self.assertEqual(body, (b'',))


class LinkTestCase(TestCase):

    def test_node_can_link_sub_nodes(self):
        root, a, b = Node(), Node(), Node()
        root.link(a)
        root.link(b)
        self.assertEqual(root.nodes, [a, b])

    def test_node_cannot_link_to_node_classes(self):
        root = Node()
        with self.assertRaises(TypeError) as context:
            root.link(Node)
        self.assertEqual(str(context.exception), 'A node can only link to node instances.')

    def test_node_cannot_link_to_itself(self):
        node = Node()
        with self.assertRaises(BadLink) as context:
            node.link(node)
        self.assertEqual(str(context.exception), 'A node cannot link to itself.')

    def test_link_cannot_form_an_infinite_loop(self):
        a, b, c = Node(), Node(), Node()
        a.link(b)
        b.link(c)
        with self.assertRaises(BadLink) as context:
            c.link(a)
        self.assertEqual(str(context.exception), 'A node link must not form a path to itself.')


class SubmitTestCase(TestCase):

    def test_submit_accepts_request_and_returns_response(self):
        node = Node()
        request = Request({})
        response = node.submit(request)
        self.assertIsInstance(response, Response)

    def test_submit_can_be_called_with_previously_created_response(self):
        node = Node()
        request = Request({})
        original_response = Response()
        response = node.submit(request, original_response)
        self.assertIs(response, original_response)

    def test_submit_calls_node_handle(self):
        node = Node()
        node.handle = Mock(return_value=Response())
        request = Request({})
        response = node.submit(request)
        self.assertEqual(node.handle.call_count, 1)

    def test_returned_response_can_be_altered_by_handle_return(self):
        node = Node()
        handle_response = Response()
        node.handle = Mock(return_value=handle_response)
        request = Request({})
        response = node.submit(request)
        self.assertIs(response, handle_response)

    def test_raises_exception_if_handle_does_not_return_response(self):
        node = Node()
        node.handle = Mock()
        request = Request({})
        with self.assertRaises(BadHandle) as context:
            node.submit(request)
        self.assertEqual(str(context.exception), 'Node handle did not return or raise a response.')

    def test_node_handle_can_raise_response_instead_of_returning(self):
        node = Node()
        handle_response = Response()
        node.handle = Mock(side_effect=handle_response)
        request = Request({})
        response = node.submit(request)
        self.assertIs(response, handle_response)

    def test_submit_recurses_through_sub_nodes(self):
        root, a, b = Node(), Node(), Node()
        root.link(a)
        a.link(b)
        root.handle = Mock(return_value=Response())
        a.handle = Mock(return_value=Response())
        b.handle = Mock(return_value=Response())
        request = Request({})
        root.submit(request)
        self.assertEqual(root.handle.call_count, 1)
        self.assertEqual(a.handle.call_count, 1)
        self.assertEqual(b.handle.call_count, 1)

    def test_submitted_response_stays_the_same_if_not_changed_by_the_node_recursion(self):
        root, a, b = Node(), Node(), Node()
        root.link(a)
        a.link(b)
        request = Request({})
        original_response = Response()
        response = root.submit(request, original_response)
        self.assertIs(response, original_response)

    def test_submit_on_sub_node_might_replace_response_returning_another_one(self):
        root, node = Node(), Node()
        root.link(node)
        node.handle = Mock(return_value=Response())
        request = Request({})
        original_response = Response()
        response = root.submit(request, original_response)
        self.assertIsNot(response, original_response)

    def test_sub_nodes_are_not_called_if_response_is_raised_from_node_handle(self):
        root, node = Node(), Node()
        root.link(node)
        root.handle = Mock(side_effect=Response())
        node.submit = Mock()
        request = Request({})
        root.submit(request)
        self.assertEqual(node.submit.call_count, 0)


class HandleTestCase(TestCase):

    def test_node_handle_accepts_request_and_response(self):
        node = Node()
        request = Request({})
        response = Response()
        node_response = node.handle(request, response)
        self.assertIs(node_response, response)
