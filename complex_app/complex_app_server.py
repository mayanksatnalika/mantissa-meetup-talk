import time
from flask import Flask, jsonify, make_response, request
from model import more_magical_prediction_function

app = Flask(__name__)


def is_valid_body(request):
    try:
        body = request.json
        if "field1" not in body:
            return (False, "key field1 not found in body.")
        if "field2" not in body:
            return (False, "key field2 not found in body.")
    except Exception as e:
        return (False, e)
    return (True, "Ok")


@app.route('/')
def index():
    return "<h2>Hi! from my app</h2>"


@app.route('/classify', methods=['PUT'])
def classify():
    if not request.json:
        return make_response(jsonify(
            {"error": "Failed not json "}
        ), 400)
    body_is_valid = is_valid_body(request)
    if body_is_valid[0] is False:
        return make_response(jsonify(
            {"error": "Invalid body: {err}.".format(err=body_is_valid[1])}
        ), 422)

    ans = more_magical_prediction_function(request.json)
    return make_response(jsonify(
        {"ans": ans}
    ), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
