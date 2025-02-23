from contact_book.shared.global_strings import pagination_route_path
from contact_book.src.api.contacts.utils import phn

base_api_url = "/contacts"

from sqlalchemy import text

def clear_db(db):
    db.execute(text("DELETE FROM contacts"))
    db.commit()

def create_json_contact_for_test(first_name="John", last_name="Doe", phone_number=None, address="123 Main St"):
    if phone_number is None:
        phone_number = phn()
    return {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "address": address
    }


def create_contact_with_api(client, first_name="John", last_name="Doe", phone_number=None, address="123 Main St"):
    json_contact = create_json_contact_for_test(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        address=address
    )
    response = client.post(base_api_url, json=json_contact)

    # 🔥 Debug: Print response if the request fails
    if response.status_code != 200:
        print("❌ Request Failed")
        print("Request JSON:", json_contact)
        print("Response JSON:", response.json())  # Print FastAPI validation errors

    assert response.status_code == 200, response.text
    return response.json()


def test_create_single_contact(client):
    data = create_contact_with_api(client=client)
    contact_id = data["id"]
    assert data["first_name"] == "John"

    # Here you can query the database directly if needed:
    response = client.get(f"{base_api_url}/{contact_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id

def test_get_contact(client):
    data = create_contact_with_api(client=client)
    contact_id = data["id"]
    response = client.get(f"{base_api_url}/{contact_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id

def test_get_pagination(client):
    for i in range(5):
        create_contact_with_api(client=client, first_name=f"John_{i}")

    response = client.get(f"{base_api_url}{pagination_route_path}", params={"page": 1})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5

    response = client.get(f"{base_api_url}{pagination_route_path}", params={"page": 0})
    assert response.status_code == 400

def test_delete_contact(client):
    data = create_contact_with_api(client=client)
    contact_id = data["id"]
    response = client.delete(f"{base_api_url}/{contact_id}")
    assert response.status_code == 200
    seconds_response = client.get(f"{base_api_url}/{contact_id}")
    assert seconds_response.status_code == 404

def test_update_contact(client):
    data = create_contact_with_api(client=client)
    contact_id = data["id"]
    response = client.put(f"{base_api_url}/{contact_id}", json={"first_name": "Jane"})
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"

    # Verify on get
    response = client.get(f"{base_api_url}/{contact_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"

def test_search_contact(client):
    create_contact_with_api(client=client, first_name="John", last_name="Doe", phone_number="123")
    create_contact_with_api(client=client, first_name="Jane", last_name="Smith")
    create_contact_with_api(client=client, first_name="John", last_name="Smith")
    create_contact_with_api(client=client, first_name="Jane", last_name="Doe")

    response = client.get(f"{base_api_url}/search", params={"first_name": "John"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    response = client.get(f"{base_api_url}/search", params={"last_name": "Doe"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    response = client.get(f"{base_api_url}/search", params={"first_name": "John", "last_name": "Doe"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    response = client.get(f"{base_api_url}/search", params={"first_name": "Jane", "last_name": "Smith"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    response = client.get(f"{base_api_url}/search", params={"first_name": "John", "last_name": "Smith"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    response = client.get(f"{base_api_url}/search", params={"first_name": "Jane", "last_name": "Doe"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    response = client.get(f"{base_api_url}/search", params={"first_name": "John", "last_name": "Doe", "phone_number": "123"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    response = client.get(f"{base_api_url}/search", params={"first_name": "John", "last_name": "Doe", "phone_number": "456"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0