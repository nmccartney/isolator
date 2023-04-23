# -*- encoding: utf-8 -*-

from .config import BaseConfig
from threading import Timer

from flask import request
from flask_restx import Api, Resource, fields, reqparse

sampleParser = reqparse.RequestParser()
sampleParser.add_argument("sample", type=dict, help="sample should be json")


rest_api = Api(version="1.0", title="Mock Vehicle API")

sio = None
celery  =  None

def setup_routes(app, io, c):
    rest_api.init_app(app)
    global sio
    sio = io
    global celery
    celery = c


"""
    Helpers
"""


"""
    Flask-Restx routes
"""


@rest_api.route('/health')
class Health(Resource):
    """
       health check
    """

    def get(self):
        # sio.emit('vehicle/health', {'id': 'flappy-bird'})
        return {"ok": True, "success": True, }, 200



@rest_api.route('/samples')
class Samples(Resource):
    """
       samples
    """
    samples = []
    curr_sample = None

    def get(self):
        sample = self.curr_sample  # missionManager.get()
        return {"ok": True, "success": True, "mission": mission}, 200

    @rest_api.expect(sampleParser)
    def post(self):
        sample = sampleParser.parse_args()['sample']
        # mission = missionManager.add()
        # self.curr_mission = mission  # {"waypoints": [], "geofences": []}
        # print('Got new sample', mission)

        return {"ok": True, "success": True, "sample": self.curr_mission}, 200
