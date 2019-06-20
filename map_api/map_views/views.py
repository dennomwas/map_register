from flask import Blueprint, request, json, jsonify, g, url_for
from flask_restful import Api, Resource
from flask_paginate import Pagination
from sqlalchemy import and_, or_

# local imports
from map_api.models import MapRegister, auth, db
from map_api.utils.schemas import MapRegisterSchema
from map_api.utils.paginate import paginate_items
from map_api.map_auth.views import AuthRequiredResource

map_blueprint = Blueprint('map_blueprint', __name__)
map_schema = MapRegisterSchema()
api = Api(map_blueprint)


class MapRegisterResource(AuthRequiredResource):
    def post(self):
        '''
        get user data
        check for errors
        check for duplicates
        post to db
        '''
        payload = request.get_json()

        if payload:
            result, errors = map_schema.load(payload)

            if errors:
                return jsonify(errors, 404)

            map_name = payload['map_name']
            map_type = payload['map_type']
            sheet_no = payload['sheet_no']
            fr_no = payload['fr_no']
            lr_no = payload['lr_no']

            existing_RIM_map = MapRegister.query.filter(
                and_(
                    MapRegister.map_name == map_name,
                    MapRegister.map_type == map_type,
                    MapRegister.sheet_no == sheet_no)
            ).all()
            if existing_map:
                return jsonify({'error': 'Map already exists'})

            existing_survey_plan_map = MapRegister.query.filter(
                and_(MapRegister.map_name == map_name,
                     MapRegister.map_type == map_type,
                     MapRegister.lr_no == lr_no,
                     MapRegister.fr_no == fr_no)
            ).all()

            if existing_survey_plan_map:
                return jsonify({'error': 'Map already exists'})

            map_data = MapRegister(
                serial_no=result['serial_no'],
                area=result['area'],
                locality=result['locality'],
                map_name=result['map_name'],
                map_type=result['map_type'],
                lr_no=result['lr_no'],
                fr_no=result['fr_no'],
                sheet_no=result['sheet_no'],
                created_by=g.user.id or None
            )
            map_data.save()
            return jsonify({'message': 'Map successfully added'}, 201)
        else:
            return jsonify({'error': 'Please Check your fields and try again'}, 404)

    def get(self):

        search_term = request.args.get('q')

        if search_term:
            search_results = MapRegister.query.filter(
                or_(MapRegister.map_name.ilike('%' + search_term + '%'),
                    MapRegister.area.ilike('%' + search_term + '%'),
                    MapRegister.locality.ilike('%' + search_term + '%'))
            ).all()

            if not search_results:
                return jsonify({'error': 'Your search did not yield any results'}, 404)

            results = map_schema.dump(search_results, many=True).data
            return jsonify({'results': results})

        else:
            data = paginate_items(MapRegister, map_schema)
            return data


class MapRegisterItemResource(AuthRequiredResource):
    def get(self, id):
        map_item = MapRegister.query.get(id)

        if not map_item:
            return jsonify({'error': 'Map is not Available'})

        result = map_schema.dump(map_item).data
        return result

    def put(self, id):

        payload = request.get_json()
        if not payload:
            return jsonify({'error': 'Details to update must be Provided'})

        map_item = MapRegister.query.get(id)
        if not map_item:
            return jsonify({'error': 'Map is not Available'})

        if payload.get('area'):
            map_item.area = payload['area']

        if payload.get('locality'):
            map_item.locality = payload['locality']

        if payload.get('map_name'):
            map_item.map_name = payload['map_name']

        if payload.get('map_type'):
            map_item.map_type = payload['map_type']

        if payload.get('lr_no'):
            map_item.lr_no = payload['lr_no']

        if payload.get('fr_no'):
            map_item.fr_no = payload['fr_no']

        if payload.get('sheet_no'):
            map_item.sheet_no = payload['sheet_no']

        if payload.get('modified_by'):
            map_item.modified_by = payload['modified_by']

        map_item.update()
        return jsonify({'message': 'Map Updated successfully'})

    def delete(self, id):
        map = MapRegister.query.get(id)

        if not map:
            return jsonify({'error': 'Map is not Available'})

        map.delete()
        return jsonify({'message': 'Map Deleted Successfully'})


api.add_resource(MapRegisterResource, '', '/', endpoint='mapregister')
api.add_resource(MapRegisterItemResource, '/<string:id>', '/<string:id>/',
                 endpoint='mapregisteritem')
