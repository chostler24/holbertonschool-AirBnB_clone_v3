#!/usr/bin/python3
"""
    new view for City objs in RESTFul API
"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from sqlalchemy.exc import IntegrityError


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def city_list(state_id):
    """retrieves list of city objects"""
    dict_state = storage.all(State)
    list_city = None
    city_list = []
    for state_get in dict_state.values():
        if state_get.id == state_id:
            list_city = state_get.cities
    if list_city is None:
        abort(404)
    for city_get in list_city:
        city_list.append(city_get.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_get(city_id):
    """retrieves a city object"""
    city_get = storage.get(City, city_id)
    if city_get is not None:
        return jsonify(city_get.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    """deletes a city object"""
    city_get = storage.get(City, city_id)
    if city_get is not None:
        storage.delete(city_get)
        storage.save()
        return make_response(
            jsonify({}), 200
        )
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_create(state_id):
    """creates a city object"""
    try:
        req = request.get_json()
        if req is not None:
            if 'name' in req.keys() and req['name'] is not None:
                req['state_id'] = state_id
                new = City(**req)
                new.save()
                return make_response(jsonify(new.to_dict()), 201)
            return make_response(jsonify({
                'error': 'Missing name'
                }), 400)
        return make_response(jsonify({
            "error": "Not a JSON"
            }), 400)
    except IntegrityError:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def city_update(city_id):
    """updates a city object"""
    req = request.get_json()
    if req is not None:
        check_city = storage.get(City, city_id)
        if check_city is None:
            abort(404)
        for key, val in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(check_city, key, val)
        storage.save()
        return make_response(jsonify(check_city.to_dict()), 200)
    return make_response(jsonify({
        "error": "Not a JSON"
        }), 400)
