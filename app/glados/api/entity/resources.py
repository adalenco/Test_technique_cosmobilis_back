from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer, EntityUpdateSerializer, EntityPostSerializer, EntityDeleteSerializer
from glados.repositories.entities import get_entities, update_entity, post_entity, delete_entity


class EntitiesAPI(Resource):
    def get(self):
        request_serializer = EntitiesRequestSerializer()
        data = request_serializer.load(request.args)

        entities = get_entities(data)

        serializer = EntityResponseSerializer(many=True)
        return serializer.dump(entities), 200

    def patch(self):
        entity_id = request.args.get("id")
        request_serializer = EntityUpdateSerializer()
        try:
            update_data = request_serializer.load(request.json)
        except ValidationError as err:
            return {"error": err.messages}, 400

        updated_entity = update_entity(entity_id, update_data)

        if not updated_entity:
            return {"error": "Entity not found"}, 404

        response_serializer = EntityResponseSerializer()
        return response_serializer.dump(updated_entity), 200

    def post(self):
        request_serializer = EntityPostSerializer()
        data = request_serializer.load(request.json)

        entity = post_entity(data)

        if entity == "error sql":
            return {"error": "Database error"}, 500
        elif entity == "error room":
            return {"error": "No room with this id"}, 404
        elif entity == "error name":
            return {"error": "Name already exists"}, 400

        response_serializer = EntityResponseSerializer()
        return response_serializer.dump(entity), 200

    def delete(self):
        request_serializer = EntityDeleteSerializer()
        data = request_serializer.load(request.args)
        result = delete_entity(data)

        if result is False:
            return {"error": "Entity not found"}, 404

        return {}, 204
