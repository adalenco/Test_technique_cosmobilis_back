from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer, EntityUpdateSerializer
from glados.repositories.entities import get_entities, update_entity


class EntitiesAPI(Resource):
    def get(self):
        request_serializer = EntitiesRequestSerializer()
        data = request_serializer.load(request.args)

        entities = get_entities(data)

        serializer = EntityResponseSerializer(many=True)
        return serializer.dump(entities), 200

    def patch(self):
        # Charger et valider les données de la requête
        entity_id = request.args.get("id")
        request_serializer = EntityUpdateSerializer()
        try:
            update_data = request_serializer.load(request.json)  # Charger depuis le body JSON
        except ValidationError as err:
            return {"error": err.messages}, 400

        # Appliquer la mise à jour
        updated_entity = update_entity(entity_id, update_data)

        if not updated_entity:
            return {"message": "Entity not found"}, 404

        # Sérialiser la réponse
        response_serializer = EntityResponseSerializer()
        return response_serializer.dump(updated_entity), 200
