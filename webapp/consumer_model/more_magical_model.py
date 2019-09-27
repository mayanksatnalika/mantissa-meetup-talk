from logging_helper.logging_helper import create_logger
import time
import pika
import json
import pymongo
from bson.objectid import ObjectId
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbit'))
channel = connection.channel()


logger = create_logger(__name__, stdout_handler=True)

client = pymongo.MongoClient(host="mongo", port=27017)
db_conn = client['mantissa_web_app']


def more_magical_prediction_function(input1, input2):
    print "will sleep..."
    time.sleep(10)
    return input1*input2


def callback(channel, method_frame, header_frame, body):
    logger.info("recieved, now sleeping...")
    message = json.loads(body)
    answer = more_magical_prediction_function(message['input_number1'], message['input_number1'])
    logger.info("Answer is {ans}".format(ans=answer))
    query_ = {"_id": ObjectId(message['msg_id'])}
    payload = {"model_answer": answer}
    db_conn['some_collection'].update_one(query_, {"$set": payload})
    logger.info("Saved!")
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == "__main__":

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume('mantisaa_task_queue', callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
