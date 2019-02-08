# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from . import elevator


class FloorFloorIdCarFind(Resource):

    def get(self, floor_id):
        car_id = elevator.find_closest_car(floor_id)
        car_name = elevator.car_map[car_id]
        return {'car_id': car_id,
                'car_name': car_name.decode('utf-8')}, 200, None
