# -*- encoding: utf-8 -*-

from threading import Timer
import json
import time
import socket


import socketio as io
from flask import Flask
from flask_socketio import SocketIO, send, emit

from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from celery import Celery
from celery.result import AsyncResult
from celery.exceptions import TimeoutError
from celery.decorators import task, periodic_task

from .models import db
from .routes import rest_api, setup_routes

app = Flask(__name__)

app.config.from_object('api.config.BaseConfig')

# File  upload   config
app.config['UPLOAD_FOLDER'] = '/musicFiles/'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
# app.config['MAX_CONTENT_PATH']
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 1000  # 50MB

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(
    app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

ioServer = SocketIO(app, cors_allowed_origins='*')

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mock-Vehicle"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

# SocketIO AS A SERVER


@ioServer.on('connect')
def handle_connection(message):
    print('got connection!', message)


@ioServer.on('disconnect')
def handle_disconnection():
    print('lost connection!')
# /End of SocketIO as a SERVER

db.init_app(app)
# rest_api.init_app(app)
setup_routes(app, ioServer, celery)
CORS(app)

# standard Python

"""
   Custom responses
"""


@app.after_request
def after_request(response):
    """
       Sends back a custom error with {"success", "msg"} format
    """

    if int(response.status_code) >= 400:
        response_data = json.loads(response.get_data())
        if "errors" in response_data:
            response_data = {"success": False,
                             "msg": list(response_data["errors"].items())[0][1]}
            response.set_data(json.dumps(response_data))
        response.headers.add('Content-Type', 'application/json')
    return response
