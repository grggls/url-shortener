"""
You can auto-discover and run all tests with this command:

    $ pytest

Documentation:

* https://docs.pytest.org/en/latest/
* https://docs.pytest.org/en/latest/fixture.html
* http://flask.pocoo.org/docs/latest/testing/
"""

import pytest
from main import app

# test the root doc, API should respond if pinged
def test_get_root_url():
    res = app.test_client().get("/")
    assert res.status_code == 200
    assert b"Hello, Url Shortener" in res.data


# test basic encoding
def test_encode_url():
    res = app.test_client().post("/encode?url=https://google.com")
    assert res.status_code == 200
    assert b"encode" in res.data
    assert b"google.com" in res.data
    assert b"result" in res.data


# test decoding for key not found
def test_key_not_found():
    res = app.test_client().get("/decode/foo")
    assert res.status_code == 200
    assert b"decode" in res.data
    assert b"result" in res.data
    assert b"shortened URL not found" in res.data


# test full encode/decode conversation
def test_decode_id():
    # encode
    res = app.test_client().post("/encode?url=https://www.finn.com")
    assert res.status_code == 200
    assert res.json["encode"] == "https://www.finn.com"
    result = res.json["result"]

    # decode
    res = app.test_client().get("/decode/" + result)
    assert res.status_code == 200
    assert b"decode" in res.data
    assert res.json["result"] == "https://www.finn.com"


# test full encode/decode conversation with a more challenging urlstring
def test_encode_challenging_url():
    # encode
    res = app.test_client().post("/encode?url=https://www.finn.com/en-US/pdp/tesla-model3-680-midnightsilvermetallic")
    assert res.status_code == 200
    assert res.json["encode"] == "https://www.finn.com/en-US/pdp/tesla-model3-680-midnightsilvermetallic"
    result = res.json["result"]

    # decode
    res = app.test_client().get("/decode/" + result)
    assert res.status_code == 200
    assert b"decode" in res.data
    assert res.json["result"] == "https://www.finn.com/en-US/pdp/tesla-model3-680-midnightsilvermetallic"


# test bad urls
def test_bad_urls():
    res = app.test_client().post("/encode?url=foo")
    assert res.status_code == 400
    res = app.test_client().post("/encode?url=https://foo")
    assert res.status_code == 200
    res = app.test_client().post("/encode?url= ")
    assert res.status_code == 400


# test bad verbs
def test_bad_methods():
    res = app.test_client().get("/encode?url=google.com")
    assert res.status_code == 405
    res = app.test_client().post("/decode/0xdeadbeef")
    assert res.status_code == 405   
    res = app.test_client().put("/encode?url=google.com")
    assert res.status_code == 405
    res = app.test_client().delete("/encode?url=google.com")
    assert res.status_code == 405
    res = app.test_client().patch("/encode?url=google.com")
    assert res.status_code == 405


