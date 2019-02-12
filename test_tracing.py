# -*- coding: utf-8 -*-
import uuid

import flask
import pytest

from flask_tracing import Tracing


@pytest.fixture
def app(request):
    app = flask.Flask(request.module.__name__)
    app.testing = True
    Tracing(app)

    @app.route('/')
    def index():
        return 'hello world.'

    return app


def test_add_request_id(app):
    with app.test_client() as c:
        rv = c.get('/')
        assert 'X-Request-ID' in rv.headers
        request_id = rv.headers.get('X-Request-ID')
        assert len(request_id) == 36
        assert len(request_id.split('-')) == 5


def test_append_trace_id(app):
    with app.test_client() as c:
        original_id = uuid.uuid4()
        rv = c.get('/', headers={
            'X-Request-ID': original_id
        })
        assert 'X-Request-ID' in rv.headers
        request_ids = rv.headers.get('X-Request-ID')
        assert len(request_ids.split(',')) == 2
        old, new = request_ids.split(',')
        assert old == str(original_id)
