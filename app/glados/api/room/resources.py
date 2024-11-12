from flask import request
from flask_restful import Resource

from glados.api.room.serializers import RoomResponseSerializer, RoomPostSerializer, RoomDeleteSerializer
from glados.repositories.rooms import get_rooms, post_room, delete_room


class RoomsAPI(Resource):
    def get(self):
        rooms = get_rooms()

        serializer = RoomResponseSerializer(many=True)
        return serializer.dump(rooms), 200

    def post(self):
        request_serializer = RoomPostSerializer()
        data = request_serializer.load(request.json)

        room = post_room(data)

        if room == "error sql":
            return {"error": "Database error"}, 500
        elif room == "error name":
            return {"error": "Name already exists"}, 400

        serializer = RoomResponseSerializer(many=False)
        return serializer.dump(room), 200

    def delete(self):
        request_serializer = RoomDeleteSerializer()
        data = request_serializer.load(request.args)
        result = delete_room(data)

        if result is False:
            return {"error": "Room not found"}, 404
        return {}, 204
