import secrets
import string
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging as logger
import validators


# create a simple lambda for generating short, random strings 9 bytes long
chars  = string.ascii_uppercase + string.digits
encode = lambda _: "".join(secrets.choice(chars) for _ in range(9))

# keeping shortened urls in memory for now, not concerned with persistence
url_database = {}


def create_app(config=None):
    app = Flask(__name__)

    # See http://flask.pocoo.org/docs/latest/config/
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    # Setup cors headers to allow all domains to smooth testing
    # https://flask-cors.readthedocs.io/en/latest/
    CORS(app)


    # Definition of the routes. Put them into their own file. See also
    # Flask Blueprints: http://flask.pocoo.org/docs/latest/blueprints
    @app.route("/")
    def root_url():
        logger.info("/")
        return "Hello, Url Shortener"


    @app.route("/encode", methods=['POST'])
    def encode_url_arg():
        args = request.args
        url = args.to_dict().get("url")
        
        # don't store invalid or malformed urls. allow for users to omit "https://"
        if not validators.url(url) and not validators.url("https://" + url):
          return "invalid URL", 400

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

    
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app = create_app()
    app.run(host="0.0.0.0", port=port)

