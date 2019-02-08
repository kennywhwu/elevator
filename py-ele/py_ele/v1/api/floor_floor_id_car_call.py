# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from . import elevator


class FloorFloorIdCarCall(Resource):

    def get(self, floor_id):
        # Notification message of identified car arriving at specified floor
        return {'msg': f"{elevator.call_car(floor_id).decode('utf-8')} has arrived at floor {elevator.floor_map[floor_id]}"}, 200, None
