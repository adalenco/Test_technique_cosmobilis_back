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


def post_entity(data):
    name = data.get("name")
    type = data.get("type")
    status = data.get("status")
    room_id = data.get("room_id")
    value = data.get("value")

    if room_id:
        try:
            room = Room.query.get(room_id)
        except exc.SQLAlchemyError:
            return "error sql"
        if not room:
            return "error room"

    try:
        entity = Entity.query.filter_by(name=name).first()
    except exc.SQLAlchemyError:
        return "error sql"
    if entity:
        return "error name"

    try:
        new_entity = Entity(name=name, type=type, status=status, value=value, room_id=room_id)
        db.session.add(new_entity)
        db.session.commit()
        return new_entity
    except exc.SQLAlchemyError:
        db.session.rollback()
        return "error sql"


def delete_entity(data):
    id = data.get("id")

    try:
        entity = Entity.query.get(id)
    except exc.SQLAlchemyError:
        return False

    if not entity:
        return False

    db.session.delete(entity)
    db.session.commit()
    return True
