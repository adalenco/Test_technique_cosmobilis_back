from flask_restful import Resource

from glados.api.room.serializers import RoomResponseSerializer
from glados.repositories.rooms import get_rooms


class RoomsAPI(Resource):
    def get(self):
        rooms = get_rooms()

        serializer = RoomResponseSerializer(many=True)
        return serializer.dump(rooms), 200
