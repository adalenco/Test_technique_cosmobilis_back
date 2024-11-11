import uuid
import pytest

from glados.models import Room


@pytest.fixture
def rooms():
    kitchen = Room(id=uuid.UUID(int=1), name="Kitchen")
    kitchen.save(commit=False)

    living_room = Room(id=uuid.UUID(int=2), name="Living Room")
    living_room.save(commit=False)


def test_get_rooms(client, rooms, mocker):
    response = client.get("/rooms")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Kitchen",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Living Room",
            "created_at": mocker.ANY
        }
    ]
