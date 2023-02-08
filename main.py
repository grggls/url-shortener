import secrets
import string
from flask import Flask, jsonify, request
import logging as logger
from urllib.parse import urlparse

# create our Flask app in the global context so we can import it to the wsgi
app = Flask(__name__)

# create a simple lambda for generating short, random strings 9 bytes long
chars  = string.ascii_uppercase + string.digits
encode = lambda _: "".join(secrets.choice(chars) for _ in range(9))

# keeping shortened urls in memory for now, not concerned with persistence
url_database = {}


# Respond to requests for the root doc for keepalive and debugging
@app.route("/")
def root_url():
    logger.info("/")
    return "Hello, Url Shortener"


@app.route("/encode", methods=['POST'])
def encode_url_arg():
    url = request.args.to_dict().get("url")
    
    # don't store invalid or malformed urls
    valid = urlparse(url)
    if valid.scheme and valid.netloc:

        # encode the URL, check that it's not already a key in the database
        # break and re-encode, or store it as necessary and reply
        while True:
          key = encode(url)
          if key in url_database:
            logger.warning("collision on key: %s", key)
            break
          else:
            url_database[key] = url
            result = jsonify({"encode": url, "result": key})
            return result

    else:
      return "invalid URL", 400

@app.route("/decode/<someId>", methods=['GET'])
def decode_id_arg(someId):
    logger.info("/decode/%s", someId)

    # check if we have someId in our url_database, return the URL or a helpful msg
    if someId in url_database:
      result = url_database[someId]
      logger.info("successful lookup for key, url: %s, %s", someId, result)
    else:
      result = "shortened URL not found"
      logger.info("key: %s not found")
    return jsonify({"decode": someId, "result": result})

