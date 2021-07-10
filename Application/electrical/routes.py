"""
Electrical
"""
from flask import render_template, Response, redirect, request, url_for
from Application.electrical import bp
import itertools
import time
from kafka import KafkaConsumer
import json


consumer = KafkaConsumer('electrical', bootstrap_servers=['127.0.0.1:9092'])


@bp.route('/electrical', methods=['GET', 'POST'])
def electrical1():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            for msg in consumer:
                val = json.loads(msg.value)
                yield "data: %d\n\n" % (val["payload"]["Kilowatt"])
                # time.sleep(.1)  # an artificial delay
        return Response(events(), content_type='text/event-stream')
    redirect('/electrical')
    return render_template('electrical.html')
