from unittest import TestCase
from io import BytesIO
import copy

from vertx import Request


class RequestTestCase(TestCase):

    def test_string_representation(self):
        env = mock_env()
        env['REQUEST_METHOD'] = 'POST'
        env['PATH_INFO'] = '/dashboard/products'
        request = Request(env)
        self.assertEqual(str(request), '<Request:POST:/dashboard/products>')
        self.assertEqual(repr(request), '<Request:POST:/dashboard/products>')

    def test_request_method(self):
        env = mock_env()
        request = Request(env)
        env['REQUEST_METHOD'] = 'POST'
        request = Request(env)
        self.assertEqual(request.method, 'POST')

    def test_url(self):
        env = mock_env()
        env['wsgi.url_scheme'] = 'https'
        env['HTTP_HOST'] = 'myserver.com:8080'
        env['PATH_INFO'] = '/dashboard/products'
        env['QUERY_STRING'] = 'page=1&order=price'
        request = Request(env)
        self.assertEqual(request.url, 'https://myserver.com:8080/dashboard/products?page=1&order=price')

    def test_base_url(self):
        env = mock_env()
        env['wsgi.url_scheme'] = 'https'
        env['HTTP_HOST'] = 'myserver.com:8080'
        env['PATH_INFO'] = '/dashboard/products'
        env['QUERY_STRING'] = 'page=1&order=price'
        request = Request(env)
        self.assertEqual(request.base_url, 'https://myserver.com:8080')

    def test_scheme(self):
        env = mock_env()
        env['wsgi.url_scheme'] = 'https'
        request = Request(env)
        self.assertEqual(request.scheme, 'https')

    def test_host(self):
        env = mock_env()
        env['HTTP_HOST'] = 'myserver.com:8080'
        request = Request(env)
        self.assertEqual(request.host, 'myserver.com:8080')

    def test_path(self):
        env = mock_env()
        env['PATH_INFO'] = '/dashboard/products'
        request = Request(env)
        self.assertEqual(request.path, '/dashboard/products')

    def test_query_string(self):
        env = mock_env()
        env['QUERY_STRING'] = 'page=1&order=price'
        request = Request(env)
        self.assertEqual(request.query_string, 'page=1&order=price')

    def test_body(self):
        env = mock_env()
        env['wsgi.input'].write(b'<h1>Hello World</h1>')
        env['wsgi.input'].seek(0)
        request = Request(env)
        self.assertEqual(request.body, b'<h1>Hello World</h1>')

    def test_query(self):
        env = mock_env()
        env['QUERY_STRING'] = 'page=1&order=price'
        request = Request(env)
        self.assertEqual(request.query, {'page': '1', 'order': 'price'})

    def test_headers(self):
        env = mock_env()
        env['HTTP_AUTH'] = 'token'
        env['HTTP_X_FORWARDED_FOR'] = '203.0.113.195, 70.41.3.18, 150.172.238.178'
        request = Request(env)
        self.assertEqual(request.headers, {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, sdch',
            'accept-language': 'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
            'auth': 'token',
            'connection': 'keep-alive',
            'host': 'localhost:8000',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
            'x-forwarded-for': '203.0.113.195, 70.41.3.18, 150.172.238.178',
        })

    def test_header_keys_are_case_insensitive(self):
        env = mock_env()
        env['HTTP_AUTH'] = 'token'
        request = Request(env)
        self.assertEqual(request.headers['auTH'], 'token')

    def test_cookies(self):
        env = mock_env()
        env['HTTP_COOKIE'] = 'foo=bar; bar=biz'
        request = Request(env)
        self.assertEqual(request.cookies, {'foo': 'bar', 'bar': 'biz'})

    def test_empty_cookies(self):
        env = mock_env()
        request = Request(env)
        self.assertEqual(request.cookies, {})

    def test_cookie_with_special_characters(self):
        env = mock_env()
        env['HTTP_COOKIE'] = 'token="abc/\\073\\054~\\341\\347[\'!\\"\\"]"'
        request = Request(env)
        self.assertEqual(request.cookies, {'token': 'abc/;,~áç[\'!""]'})

    def test_ip(self):
        env = mock_env()
        env['REMOTE_ADDR'] = '127.0.0.1'
        request = Request(env)
        self.assertEqual(request.ip, '127.0.0.1')

    def test_ip_with_x_forwarded_for_header(self):
        env = mock_env()
        env['HTTP_X_FORWARDED_FOR'] = '203.0.113.195, 70.41.3.18, 150.172.238.178'
        request = Request(env)
        self.assertEqual(request.ip, '203.0.113.195')

    def test_referer(self):
        env = mock_env()
        env['HTTP_REFERER'] = 'http://localhost:8000/app/hello'
        request = Request(env)
        self.assertEqual(request.referer, 'http://localhost:8000/app/hello')

    def test_empty_referer(self):
        env = mock_env()
        request = Request(env)
        self.assertIsNone(request.referer)

    def test_user_agent(self):
        env = mock_env()
        request = Request(env)
        self.assertEqual(request.user_agent, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')

    def test_empty_user_agent(self):
        env = mock_env()
        env.pop('HTTP_USER_AGENT')
        request = Request(env)
        self.assertEqual(request.user_agent, None)



def mock_env():
    return copy.deepcopy(sample_env)


sample_env = {
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'HTTP_ACCEPT_ENCODING': 'gzip, deflate, sdch',
    'HTTP_ACCEPT_LANGUAGE': 'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
    'HTTP_CONNECTION': 'keep-alive',
    'HTTP_HOST': 'localhost:8000',
    'HTTP_UPGRADE_INSECURE_REQUESTS': '1',
    'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'PATH_INFO': '',
    'QUERY_STRING': '',
    'RAW_URI': '',
    'REMOTE_ADDR': '127.0.0.1',
    'REMOTE_PORT': '54130',
    'REQUEST_METHOD': 'GET',
    'SCRIPT_NAME': '',
    'SERVER_NAME': '127.0.0.1',
    'SERVER_PORT': '8000',
    'SERVER_PROTOCOL': 'HTTP/1.1',
    'SERVER_SOFTWARE': 'gunicorn/19.6.0',
    'wsgi.errors': BytesIO(),
    'wsgi.file_wrapper': BytesIO(),
    'wsgi.input': BytesIO(),
    'wsgi.multiprocess': False,
    'wsgi.multithread': False,
    'wsgi.run_once': False,
    'wsgi.url_scheme': 'http',
    'wsgi.version': (1, 0),
}
