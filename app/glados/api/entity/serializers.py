from marshmallow import fields, validate

from glados import ma, constants
from glados.models import Entity
from glados.api.room.serializers import RoomSerializer


class EntitiesRequestSerializer(ma.Schema):
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    room = fields.String(required=False)
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    id = fields.String(required=False)


class EntitySerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")
    room = fields.Nested(RoomSerializer, allow_none=True)

    class Meta:
        model = Entity
        ordered = True
        fields = [
            "id",
            "name",
            "type",
            "status",
            "value",
            "room",
            "created_at"
        ]


class EntityResponseSerializer(EntitySerializer):
    pass


class EntityUpdateSerializer(ma.Schema):
    name = fields.String(required=False, validate=validate.Length(min=1))
    value = fields.String(required=False)
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))


class EntityPostSerializer(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    value = fields.String(required=False)
    status = fields.String(required=True, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    type = fields.String(required=True, validate=validate.OneOf([x.name for x in constants.EntityType]))
    room_id = fields.String(required=False, validate=validate.Length(min=1))


class EntityDeleteSerializer(ma.Schema):
    id = fields.String(required=True, validate=validate.Length(min=1))
