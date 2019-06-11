from flask import Blueprint
from flask_restful import Api, Resource

# local imports
from map_api.models import MapRegister
from map_api.utils.schemas import MapRegisterSchema

map_blueprint = Blueprint('map_blueprint', __name__)
map_schema = MapRegisterSchema()
api = Api(map_blueprint)

class MapRegisterResource(Resource):
    def get(self):
        map = {
            'name': 'mwas'
        }
        return map

api.add_resource(MapRegisterResource, '/' )