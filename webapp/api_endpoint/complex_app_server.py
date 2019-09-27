import json
from bson.objectid import ObjectId
import sys
import pika
import time
from bson.objectid import ObjectId

from flask import Flask, jsonify, make_response, request
from model import more_magical_prediction_function
import pymongo
app = Flask(__name__)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbit'))
channel = connection.channel()

channel.queue_declare(queue='mantisaa_task_queue', durable=True)


def is_valid_body(request):
    try:
        body = request.json
        if "input_number1" not in body:
            return (False, "key input_number not found in body.")
        if "input_number2" not in body:
            return (False, "key input_number2 not found in body.")
    except Exception as e:
        return (False, e)
    return (True, "Ok")


@app.route('/')
def index():
    return "<h2>Hi! from my app</h2>"


@app.route('/predict', methods=['POST'])
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
    message = request.json

    client = pymongo.MongoClient(host="mongo", port=27017)
    db_conn = client['mantissa_web_app']
    id_ = db_conn['some_collection'].insert_one(message)

    push_message = {}
    push_message.update({"msg_id": str(id_.inserted_id),
                         "input_number1": message['input_number1'],
                         "input_number2": message['input_number2']})

    channel.basic_publish(
        exchange='',
        routing_key='mantisaa_task_queue',
        body=json.dumps(push_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    return make_response(jsonify(
        {"ans": str(id_.inserted_id)}
    ), 200)


@app.route('/get_answer/<saveid>', methods=['GET'])
def getanswer(saveid):
    client = pymongo.MongoClient(host="mongo", port=27017)
    db_conn = client['mantissa_web_app']
    value = db_conn['some_collection'].find_one({"_id": ObjectId(saveid)})
    if "model_answer" not in value:
        return make_response(jsonify(
            {"ans": "WAIT"}
        ), 200)

    return make_response(jsonify(
        {"ans": value['model_answer']}
    ), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
