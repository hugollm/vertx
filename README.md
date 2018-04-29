# VertX

Compose modular wsgi applications in a graph, linking minimal request processors called nodes.


## Hello World

```python
# app.py
from vertx import Node


class Hello(Node):

    http_method = 'get'
    http_path = '/'

    def handle(self, request, response):
        response.status = 200
        response.body = 'hello world'
        return response


hello = Hello() # gunicorn app:hello
```
