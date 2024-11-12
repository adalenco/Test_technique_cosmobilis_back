import uuid
import pytest

from glados import constants
from glados.models import Entity, Room


@pytest.fixture
def entities():
    kitchen = Room(id=uuid.UUID(int=1), name="Kitchen")
    kitchen.save(commit=False)

    living_room = Room(id=uuid.UUID(int=2), name="Living Room")
    living_room.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=1),
        name="Ceiling Light",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.off.name,
        value=None,
        room_id=kitchen.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=2),
        name="Lamp",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.on.name,
        value=200,
        room_id=living_room.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=3),
        name="Thermometer",
        type=constants.EntityType.sensor.name,
        status=constants.EntityStatus.on.name,
        value=28,
        room_id=living_room.id)
    entity.save(commit=False)


def test_get_entities_with_invalid_type(client):
    response = client.get("/entities?type=invalid")

    assert response.status_code == 422
    assert response.json == {"errors": {
        "type": ["Must be one of: sensor, light, switch, multimedia, air_conditioner."]
    }}


def test_get_entities_with_invalid_status(client):
    response = client.get("/entities?status=invalid")

    assert response.status_code == 422
    assert response.json == {"errors": {
        "status": ["Must be one of: on, off, unavailable."]
    }}


def test_get_entities(client, entities, mocker):
    response = client.get("/entities")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "room": {
                "id": "00000000-0000-0000-0000-000000000001",
                "name": "Kitchen",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "room": {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "room": {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        }
    ]


def test_get_entities_with_type_filter(client, entities, mocker):
    response = client.get("/entities?type=sensor")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "room": {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        }
    ]


def test_get_entities_with_status_filter(client, entities, mocker):
    response = client.get("/entities?status=on")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "room": {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "room": {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        }]


def test_get_entities_with_room_filter_with_invalid_room(client, entities):
    response = client.get("/entities?room=off")

    assert response.status_code == 200
    assert response.json == []


def test_get_entities_with_room_filter(client, entities, mocker):
    response = client.get("/entities?room=Kitchen")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "room": {
                "id": "00000000-0000-0000-0000-000000000001",
                "name": "Kitchen",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        }
    ]


def test_patch_entities_by_id_with_unknown_id(client, entities):
    response = client.patch("/entities?id=dummy", json={"status": "on"})

    assert response.status_code == 404
    assert response.json == {
        "error": "Entity not found"
    }


def test_patch_entities_by_id(client, entities, mocker):
    response = client.patch("/entities?id=00000000-0000-0000-0000-000000000001", json={"status": "on"})

    assert response.status_code == 200
    assert response.json == {
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "Ceiling Light",
        "type": "light",
        "status": "on",
        "value": None,
        "room": {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Kitchen",
            "created_at": mocker.ANY
        },
        "created_at": mocker.ANY
    }


def test_post_entity_with_room_id(client, entities, mocker):
    response = client.post("/entities", json={"name": "Test", "value": "0", "type": "light", "status": "on", "room_id": "00000000-0000-0000-0000-000000000001"})

    assert response.status_code == 200
    assert response.json == {
        "id": mocker.ANY,
        "name": "Test",
        "type": "light",
        "status": "on",
        "value": "0",
        "room": {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Kitchen",
            "created_at": mocker.ANY
        },
        "created_at": mocker.ANY
    }


def test_post_entity_without_room_id(client, entities, mocker):
    response = client.post("/entities", json={"name": "Test", "value": "0", "type": "light", "status": "on"})

    assert response.status_code == 200
    assert response.json == {
        "id": mocker.ANY,
        "name": "Test",
        "type": "light",
        "status": "on",
        "value": "0",
        "room": None,
        "created_at": mocker.ANY
    }


def test_post_entity_with_invalid_room_id(client, entities):
    response = client.post("/entities", json={"name": "Test", "value": "0", "type": "light", "status": "on", "room_id": "1"})

    assert response.status_code == 500
    assert response.json == {"error": "Database error"}


def test_post_entity_with_inexisting_room_id(client, entities):
    response = client.post("/entities", json={"name": "Test", "value": "0", "type": "light", "status": "on", "room_id": "00000000-0000-0000-0000-000000000008"})

    assert response.status_code == 404
    assert response.json == {"error": "No room with this id"}


def test_post_entity_with_existing_name(client, entities):
    response = client.post("/entities", json={"name": "Ceiling Light", "value": "0", "type": "light", "status": "on"})

    assert response.status_code == 400
    assert response.json == {"error": "Name already exists"}


def test_delete_entity_with_inexisting_id(client, entities):
    response = client.delete("/entities?id=00000000-0000-0000-0000-000000000008")

    assert response.status_code == 404
    assert response.json == {"error": "Entity not found"}


def test_delete_entity(client, entities):
    response = client.delete("/entities?id=00000000-0000-0000-0000-000000000001")

    assert response.status_code == 204
