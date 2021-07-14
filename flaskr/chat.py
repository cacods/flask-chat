import csv
import urllib.request

import celery
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr import socketio
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('chat', __name__)


@bp.route('/')
@login_required
def sessions():
    return render_template('chat/sessions.html')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    if 'message' in json.keys() and json['message'] == '/stock=aapl.us':
        json['user_name'] = 'bot'
        json['message'] = get_api_stock('aapl.us')
    socketio.emit('my response', json, callback=message_received)


def get_api_stock(stock):
    api_url = 'https://stooq.com/q/l/?s=' + stock + '&f=sd2t2ohlcv&h&e=csv'
    response = urllib.request.urlopen(api_url)
    rows = [row.decode() for row in response.readlines()]
    content = list(csv.reader(rows))
    return content[1][6]


def message_received(methods=['GET', 'POST']):
    print('message was received!!!')


@celery.task
def test_celery():
    return 2 + 2
