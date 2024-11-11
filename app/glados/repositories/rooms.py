from glados.models import Room


def get_rooms():
    query = Room.query
    return query
