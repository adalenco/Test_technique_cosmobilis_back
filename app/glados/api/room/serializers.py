from marshmallow import fields, validate

from glados import ma
from glados.models import Room


class RoomsRequestSerializer(ma.Schema):
    pass


class RoomSerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Room
        ordered = True
        fields = [
            "id",
            "name",
            "created_at"
        ]


class RoomResponseSerializer(RoomSerializer):
    pass


class RoomPostSerializer(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))


class RoomDeleteSerializer(ma.Schema):
    id = fields.String(required=True, validate=validate.Length(min=1))
