from flask import Blueprint
from flask_restful import Api, Resource

# local imports
from map_api.models import MapRegister, auth
from map_api.utils.schemas import MapRegisterSchema
from map_api.map_auth.views import AuthRequiredResource

map_blueprint = Blueprint('map_blueprint', __name__)
map_schema = MapRegisterSchema()
api = Api(map_blueprint)


class MapRegisterResource(AuthRequiredResource):
    def get(self):
        map = {
            'name': 'mwas'
        }
        return map

api.add_resource(MapRegisterResource, '/' )
