# -*- coding: utf-8 -*-

import flask
import pytest

from flask_tracing import Tracing


@pytest.fixture
def app(request):
    app = flask.Flask(request.module.__name__)
    app.testing = True
    Tracing(app)
    return app


def test_add_request_id(app):
    @app.route('/')
    def index():
        return 'hello world.'

    with app.test_client() as c:
        rv = c.get('/')
        assert 'X-Request-ID' in rv.headers
        request_id = rv.headers.get('X-Request-ID')
        assert len(request_id) == 36
        assert len(request_id.split('-')) == 5
