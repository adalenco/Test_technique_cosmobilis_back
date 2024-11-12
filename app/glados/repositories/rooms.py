from sqlalchemy import exc

from glados.models import Room
from glados import db


def get_rooms():
    query = Room.query
    return query


def post_room(data):
    new_room = Room(name=data["name"])
    db.session.add(new_room)
    db.session.commit()
    return new_room


def delete_room(data):
    id = data.get("id")

    try:
        room = Room.query.get(id)
    except exc.SQLAlchemyError:
        return False

    if not room:
        return False

    db.session.delete(room)
    db.session.commit()
    return True
