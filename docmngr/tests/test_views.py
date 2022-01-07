import pytest

from docmngr.models import Folder


# #########################
# #### Folder API Tests ###
# #########################


@pytest.mark.django_db(transaction=True)
def test_gets_folder(api_client, parent_folder, child_folder, deleted_folder):
    pk = parent_folder.id
    response = api_client.get(f"/folders/{pk}/", format="json")
    assert response.status_code == 200

    folders = response.data

    # Make sure deleted folder was excluded.
    assert len(response.data) == 2

    assert folders[0]["name"] == "top_1"
    assert folders[1]["name"] == "child_1 ✓"


@pytest.mark.django_db(transaction=True)
def test_gets_top_folders(api_client, parent_folder, child_folder):
    response = api_client.get("/folders/", format="json")
    assert response.status_code == 200

    folders = response.data

    assert folders[0]["name"] == "top_1"


@pytest.mark.django_db(transaction=True)
def test_404_on_nonexistent_folder(api_client):
    response = api_client.get("/folders/999/", format="json")
    assert response.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_returns_empty_folder_list(api_client):
    response = api_client.get("/folders/", format="json")
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db(transaction=True)
def test_creates_folder(api_client, parent_folder):
    folder_data = {"name": "foobar", "parent_folder": parent_folder.id}
    response = api_client.post("/folders/", folder_data, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "foobar"
    assert response.data["parent_folder"] == parent_folder.id

    created_folder = Folder.objects.get(pk=response.data["id"])
    assert created_folder.id == response.data["id"]


@pytest.mark.django_db(transaction=True)
def test_fails_to_create_folder_due_to_invalid_data(api_client):
    folder_data = {}
    response = api_client.post("/folders/", folder_data, format="json")
    assert response.status_code == 400
    assert response.data["name"][0].code == "required"


@pytest.mark.django_db(transaction=True)
def test_renames_folder(api_client, parent_folder):
    folder_data = {"name": "foobar"}
    response = api_client.put(
        f"/folders/{parent_folder.id}/", folder_data, format="json"
    )
    assert response.status_code == 200
    assert response.data["name"] == "foobar"

    updated_folder = Folder.objects.get(pk=response.data["id"])
    assert updated_folder.name == "foobar"


@pytest.mark.django_db(transaction=True)
def test_renames_folder_to_invalid_name(api_client, parent_folder):
    folder_data = {"name": "f" * 999}
    response = api_client.put(
        f"/folders/{parent_folder.id}/", folder_data, format="json"
    )
    assert response.status_code == 400
    assert response.data["name"][0].code == "max_length"


@pytest.mark.django_db(transaction=True)
def test_tries_to_rename_not_existing_folder(api_client):
    folder_data = {"name": "foobar"}
    response = api_client.put("/folders/999/", folder_data, format="json")
    assert response.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_tries_to_rename_deleted_folder(api_client, deleted_folder):
    folder_data = {"name": "foobar"}
    response = api_client.put(
        f"/folders/{deleted_folder.id}/", folder_data, format="json"
    )
    assert response.status_code == 404


# ##########################
# ### Document API Tests ###
# ##########################
@pytest.mark.django_db(transaction=True)
@pytest.mark.wip
def test_gets_document(api_client, document_1):
    pk = document_1.id
    response = api_client.get(f"/documents/{pk}/", format="json")
    assert response.status_code == 200

    document = response.data

    # Make sure deleted folder was excluded.
    assert document["title"] == "doc1"


@pytest.mark.django_db(transaction=True)
@pytest.mark.wip
def test_fails_to_get_nonexistent_document(api_client):
    response = api_client.get("/documents/999/", format="json")
    assert response.status_code == 404


@pytest.mark.django_db(transaction=True)
@pytest.mark.wip
def test_fails_to_get_deleted_document(api_client, deleted_document):
    pk = deleted_document.id
    response = api_client.get(f"/documents/{pk}/", format="json")
    assert response.status_code == 404


# ##########################
# ###   Topic API Tests  ###
# ##########################
