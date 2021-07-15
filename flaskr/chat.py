import csv
import re
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
    if 'message' in json.keys() and re.match('/stock=.+$', json['message']):
        send_api_stock_message.delay(json['message'].split('=')[1])
    else:
        socketio.emit('my response', json)


@celery.task
def send_api_stock_message(stock):
    close_quote = get_quote_from_stooq(stock)

    if close_quote == 'N/D':
        message = 'Invalid stock'
    else:
        message = f'{stock.upper()} quote is {close_quote} per share'
    socketio.emit(
        'my response', {'user_name': 'bot', 'message': message})


def get_quote_from_stooq(stock):
    api_url = 'https://stooq.com/q/l/?s=' + stock + '&f=sd2t2ohlcv&h&e=csv'
    response = urllib.request.urlopen(api_url)
    rows = [row.decode() for row in response.readlines()]
    content = list(csv.reader(rows))
    return content[1][6]  # [1][6] is for Close column
