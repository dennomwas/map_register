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
            if existing_RIM_map:
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
        map_type = request.args.get('map-type')

        if not search_term and not map_type:
            all_maps_query = MapRegister.query
            data = paginate_items(all_maps_query)
            # serialized_data = map_schema.dump(data, many=True).data
            print(data, '\n\n\n\n')
            return data

        if search_term:
            search_results_query = MapRegister.query.filter(
                or_(MapRegister.map_name.ilike('%' + search_term + '%'),
                    MapRegister.area.ilike('%' + search_term + '%'),
                    MapRegister.locality.ilike('%' + search_term + '%'))
            )
            print(search_results_query.all(), '\n\n\n')
            search_results = paginate_items(search_results_query)
            if not search_results:
                return jsonify({'error': 'Your search did not yield any results'}, 404)

            results = map_schema.dump(search_results, many=True).data
            return jsonify({'results': results})

        map_types = ['rim-map', 'survey-plan', 'topo-map']
        if map_type not in map_types:
            return jsonify({'error': 'Not a valid Map type'}, 404)

        if map_type == 'rim-map':
            rim_maps_query = MapRegister.query.filter_by(
                map_type='RIM Map')

            if rim_maps_query:
                r = paginate_items(rim_maps_query)
                results = map_schema.dump(r, many=True).data
                return jsonify({'results': results})
            return jsonify({'error': 'No RIM Maps Available'}, 404)

        elif map_type == 'survey-plan':
            survey_plans_query = MapRegister.query.filter_by(
                map_type='Survey Plan')

            if survey_plans_query:
                results = map_schema.dump(survey_plans_query, many=True).data
                return jsonify({'results': results})
            return jsonify({'error': 'No Survey Plans Available'}, 404)

        elif map_type == 'topo-map':
            topo_maps_query = MapRegister.query.filter_by(
                map_type='Topo Map')

            if topo_maps_query:
                results = map_schema.dump(topo_maps_query, many=True).data
                return jsonify({'results': results})
            return jsonify({'error': 'No Topo Maps Available'}, 404)


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
api.add_resource(MapRegisterItemResource,
                 '/<string:id>', '/<string:id>/',
                 endpoint='mapregisteritem')
