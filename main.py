"""
Simple Flask service for accepting a URL and returning a shortened string (URL).
Subsequent requests for that shortened string return the URL.

The service has two endpoints: /encode and /decode
 * /encode takes a single query string 'url', e.g. /encode?url=https://google.com
 * /decode requires a valid slug is included in the request, e.g. /decode/DEADBEEF

Both endpoints return JSON:
 * {"encode":"https://www.google.com/search","result":"GGE71A20B"}
 * {"decode":"GGE71A20B","result":"https://www.google.com/search"}

The encode endpoint minimally checks that it has received a valid URL

All URLs and shortened slugs are stored in memory. No facility is provided for persistent storage. 

This shortcoming limits our ability to run this service in a highly-available way.
"""

import secrets
import string
import logging as logger
from urllib.parse import urlparse
from flask import Flask, jsonify, request

# create our Flask app in the global context so we can import it to the wsgi
app = Flask(__name__)

def encode():
    """Generate a string of 9 random numbers and uppercase letters"""
    chars  = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(9))

# keeping shortened urls in memory for now, not concerned with persistence
url_database = {}


@app.route("/")
def root_url():
    """Respond to requests for the root doc for keepalive and debugging"""
    logger.info("/")
    return "Hello, Url Shortener"


@app.route("/encode", methods=['POST'])
def encode_url_arg():
    """Encode/store an URL and receive a slug in a JSON response"""
    url = request.args.to_dict().get("url")

    # don't store invalid or malformed urls
    valid = urlparse(url)
    if valid.scheme and valid.netloc:

        # encode the URL, check that it's not already a key in the database
        # break and re-encode, or store it as necessary and reply
        while True:
            key = encode()
            if key in url_database:
                logger.warning("collision on key: %s", key)
            else:
                url_database[key] = url
                result = jsonify({"encode": url, "result": key})
                return result

    else:
        return "invalid URL", 400


@app.route("/decode/<some_id>", methods=['GET'])
def decode_id_arg(some_id):
    """Receive a slug and return the stored URL"""
    logger.info("/decode/%s", some_id)

    # check if we have some_id in our url_database, return the URL or a helpful msg
    if some_id in url_database:
        result = url_database[some_id]
        logger.info("successful lookup for key, url: %s, %s", some_id, result)
    else:
        result = "shortened URL not found"
        logger.info("key: %s not found")
    return jsonify({"decode": some_id, "result": result})
