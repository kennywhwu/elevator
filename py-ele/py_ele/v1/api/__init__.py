# -*- coding: utf-8 -*-
import hashlib

import flask_restful as restful

from ..validators import request_validate, response_filter


class Resource(restful.Resource):
    method_decorators = [request_validate, response_filter]


class Vator(object):

    def __init__(self, floors, car_ct=1):
        self.floor_list = floors

        self.first_floor = None
        self.floor_map = {}
        for ix in range(len(floors)):
            unhashed_floor = ('floor-%s' % ix).encode('utf-8')
            fid = hashlib.sha1(unhashed_floor).hexdigest()
            self.floor_map[fid] = floors[ix]
            if self.first_floor is None:
                self.first_floor = fid

        self.car_map = {}
        self.car_current_floor = {}
        for ix in range(car_ct):
            name = ('Car-%s' % ix).encode('utf-8')
            cid = hashlib.sha1(name).hexdigest()
            self.car_map[cid] = name
            self.car_current_floor[cid] = self.first_floor

    def floor_count(self):
        return len(self.floor_list)

    def inventory(self):
        results = []
        # USE .items() INSTEAD OF .iteritems() FOR PYTHON3?
        for fid, name in self.floor_map.iteritems():
            results.append({'id': fid, 'name': name})
        # USE cid INSTEAD OF fid FOR CARS?
        for cid, name in self.car_map.iteritems():
            results.append({'id': cid, 'name': name})
        return results

    def current_floor(self, car_id):
        floor_id = self.car_current_floor[car_id]
        return {'id': floor_id, 'name': self.floor_map[floor_id]}

    def find_closest_car(self, floor_id):
        min_distance = None
        target_floor_index = self.floor_list.index(
            self.floor_map[floor_id])
        for cid in self.car_map.keys():
            car_current_floor_id = self.current_floor(cid)['id']
            if car_current_floor_id == floor_id:
                closest_car_id = cid
                break
            else:
                car_floor_index = self.floor_list.index(
                    self.floor_map[car_current_floor_id])
                if min_distance == None or abs(target_floor_index - car_floor_index) < min_distance:
                    min_distance = abs(target_floor_index - car_floor_index)
                    closest_car_id = cid
        return closest_car_id

    def call_car(self, floor_id):
        closest_car = self.find_closest_car(floor_id)
        self.car_current_floor[closest_car] = floor_id
        return self.car_map[closest_car]


elevator = Vator(['B2', 'B1', 'MZ', 'F1', 'F2',
                  'F3', 'F4', 'F5', 'F6', 'F7'], 2)
