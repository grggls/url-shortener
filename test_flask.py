"""
You can auto-discover and run all tests with this command:

    $ pytest

Documentation:

* https://docs.pytest.org/en/latest/
* https://docs.pytest.org/en/latest/fixture.html
* http://flask.pocoo.org/docs/latest/testing/
"""

import pytest

import main


@pytest.fixture
def app():
    app = main.create_app()
    app.debug = True
    return app.test_client()


def test_get_root_url(app):
    res = app.get("/")
    assert res.status_code == 200
    assert b"Hello, Url Shortener" in res.data

def test_encode_url(app):
    res = app.get("/encode/google.com")
    assert res.status_code == 200
    assert b"encode" in res.data
    assert b"google.com" in res.data
    assert b"result" in res.data
    assert b"stubbedId" in res.data


def test_decode_id(app):
    res = app.get("/decode/stubbedId")
    assert res.status_code == 200
    assert b"decode" in res.data
    assert b"stubbedId" in res.data
    assert b"result" in res.data
    assert b"stubbedUrl" in res.data
