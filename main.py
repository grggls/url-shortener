from flask import Flask, jsonify
from flask_cors import CORS
import logging as logger


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

    @app.route("/encode/<someUrl>")
    def encode_url_arg(someUrl):
        logger.info("/encode/%s", someUrl)
        return jsonify({"encode": someUrl, "result": "stubbedId"})

    @app.route("/decode/<someId>")
    def decode_id_arg(someId):
        logger.info("/decode/%s", someId)
        return jsonify({"decode": someId, "result": "stubbedUrl"})
    
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)

