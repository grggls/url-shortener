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


# test the root doc, API should respond if pinged
def test_get_root_url(app):
    res = app.get("/")
    assert res.status_code == 200
    assert b"Hello, Url Shortener" in res.data


# test basic encoding
def test_encode_url(app):
    res = app.get("/encode/google.com")
    assert res.status_code == 200
    assert b"encode" in res.data
    assert b"google.com" in res.data
    assert b"result" in res.data


# test decoding for key not found
def test_key_not_found(app):
    res = app.get("/decode/foo")
    assert res.status_code == 200
    assert b"decode" in res.data
    assert b"result" in res.data
    assert b"shortened URL not found" in res.data


# test full encode/decode conversation
def test_decode_id(app):
    # encode
    res = app.get("/encode/www.finn.com")
    assert res.status_code == 200
    assert res.json["encode"] == "www.finn.com"
    result = res.json["result"]

    # decode
    res = app.get("/decode/" + result)
    assert res.status_code == 200
    assert b"decode" in res.data
    assert res.json["result"] == "www.finn.com"
