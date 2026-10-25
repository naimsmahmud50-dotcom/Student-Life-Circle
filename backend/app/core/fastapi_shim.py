"""
========================================================================================
MODULE:    FastAPI Fallback & Portability Shim
TOPIC:     Universal Compatibility Layer for FastAPI & Starlette Primitives
FILE:      backend/app/core/fastapi_shim.py
PURPOSE:   Provides dual-resilient exports: when FastAPI is installed in production,
           it imports directly from fastapi and starlette. In lightweight test or host
           environments lacking third-party wheels, it provides transparent fallback
           classes, WebSocket handlers, and status codes, allowing unit tests and routers
           to execute without external dependencies.
AUDIENCE:  Core Architecture, Test Runners & AI Agents
STANDARDS: Zero-External-Dependency Resilience, 100% Test Portability
========================================================================================
"""

try:
    from fastapi import (
        FastAPI,
        APIRouter,
        Header,
        HTTPException,
        Query,
        status,
        Request,
        WebSocket,
        WebSocketDisconnect,
        Depends
    )
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.middleware.base import BaseHTTPMiddleware
    from fastapi.responses import JSONResponse, PlainTextResponse, Response, StreamingResponse

except ImportError:
    class WebSocketDisconnect(Exception):
        def __init__(self, code: int = 1000, reason: str = ""):
            self.code = code
            self.reason = reason
            super().__init__(f"WebSocket disconnected with code {code}: {reason}")

    class WebSocket:
        def __init__(self, query_params=None, headers=None):
            self.query_params = query_params or {}
            self.headers = headers or {}
            self.client_state = "CONNECTING"
            self._messages_in = []
            self._messages_out = []

        async def accept(self):
            self.client_state = "CONNECTED"

        async def send_json(self, data):
            self._messages_out.append(data)

        async def send_text(self, text):
            self._messages_out.append(text)

        async def receive_json(self):
            if self._messages_in:
                return self._messages_in.pop(0)
            raise WebSocketDisconnect(code=1000, reason="No more mock messages")

        async def receive_text(self):
            if self._messages_in:
                return self._messages_in.pop(0)
            raise WebSocketDisconnect(code=1000, reason="No more mock messages")

        async def close(self, code: int = 1000, reason: str = ""):
            self.client_state = "DISCONNECTED"

    class APIRouter:
        def __init__(self, *args, **kwargs):
            self.routes = []

        def include_router(self, router, **kwargs):
            pass

        def get(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator

        def post(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator

        def put(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator

        def patch(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator

        def delete(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator

        def websocket(self, path: str, *args, **kwargs):
            def decorator(f):
                return f
            return decorator


    class FastAPI(APIRouter):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.middleware_stack = []

        def add_middleware(self, middleware_class, **options):
            self.middleware_stack.append((middleware_class, options))

        def middleware(self, middleware_type: str):
            def decorator(f):
                return f
            return decorator


    def Header(default=..., **kwargs):
        return default


    def Query(default=..., **kwargs):
        return default


    def Depends(dependency=None):
        return dependency


    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str = ""):
            self.status_code = status_code
            self.detail = detail
            super().__init__(f"HTTP {status_code}: {detail}")


    class status:
        HTTP_200_OK = 200
        HTTP_201_CREATED = 201
        HTTP_204_NO_CONTENT = 204
        HTTP_400_BAD_REQUEST = 400
        HTTP_401_UNAUTHORIZED = 401
        HTTP_403_FORBIDDEN = 403
        HTTP_404_NOT_FOUND = 404
        HTTP_409_CONFLICT = 409
        HTTP_422_UNPROCESSABLE_ENTITY = 422
        HTTP_429_TOO_MANY_REQUESTS = 429
        HTTP_500_INTERNAL_SERVER_ERROR = 500
        WS_1000_NORMAL_CLOSURE = 1000
        WS_1008_POLICY_VIOLATION = 1008


    class RequestURL:
        def __init__(self, path: str = "/"):
            self.path = path

        def __str__(self):
            return self.path


    class RequestClient:
        def __init__(self, host: str = "127.0.0.1", port: int = 8000):
            self.host = host
            self.port = port


    class Request:
        def __init__(self, headers=None, client=None, url=None, method: str = "GET"):
            self.headers = headers or {}
            if client is None:
                self.client = RequestClient("127.0.0.1")
            elif isinstance(client, str):
                self.client = RequestClient(client)
            elif isinstance(client, (list, tuple)):
                self.client = RequestClient(client[0], client[1] if len(client) > 1 else 0)
            else:
                self.client = client

            if url is None:
                self.url = RequestURL("/")
            elif isinstance(url, str):
                self.url = RequestURL(url)
            else:
                self.url = url
            self.method = method


    class JSONResponse:
        def __init__(self, content, status_code: int = 200, headers=None):
            self.content = content
            self.status_code = status_code
            self.headers = headers or {}


    class Response:
        def __init__(self, content=b"", status_code: int = 200, headers=None, media_type: str = "text/plain"):
            self.content = content
            self.status_code = status_code
            self.headers = headers or {}
            self.media_type = media_type


    class PlainTextResponse(Response):
        def __init__(self, content="", status_code: int = 200, headers=None, media_type: str = "text/plain; version=0.0.4; charset=utf-8"):
            super().__init__(content=content, status_code=status_code, headers=headers, media_type=media_type)


    class StreamingResponse(Response):
        def __init__(self, content, status_code: int = 200, headers=None, media_type: str = "text/event-stream"):
            self.content_iterator = content
            super().__init__(content=b"", status_code=status_code, headers=headers, media_type=media_type)
            if headers:
                self.headers.update(headers)


    class BaseHTTPMiddleware:
        def __init__(self, app=None, dispatch=None):
            self.app = app
            self._dispatch = dispatch

        async def __call__(self, request, call_next):
            if hasattr(self, "dispatch"):
                return await self.dispatch(request, call_next)
            elif self._dispatch:
                return await self._dispatch(request, call_next)
            return await call_next(request)


    class CORSMiddleware:
        pass

