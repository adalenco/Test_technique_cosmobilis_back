from sqlalchemy import exc

from glados.models import Entity, Room
from glados import db


def get_entities(filters):
    query = Entity.query

    type = filters.get("type")
    status = filters.get("status")
    room = filters.get("room")
    id = filters.get("id")
    if type:
        query = query.filter(Entity.type == type)
    elif status:
        query = query.filter(Entity.status == status)
    elif room:
        query = query.join(Entity.room).filter(Room.name == room)
    elif id:
        query = query.filter(Entity.id == id)

    return query


def update_entity(entity_id, update_data):
    try:
        entity = Entity.query.get(entity_id)
    except exc.SQLAlchemyError:
        return None
    if not entity:
        return None

    for key, value in update_data.items():
        setattr(entity, key, value)

    db.session.commit()
    return entity
