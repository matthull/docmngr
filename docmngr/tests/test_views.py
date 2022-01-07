import pytest

from docmngr.models import Document, Folder


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
def test_fails_to_get_nonexistent_folder(api_client):
    response = api_client.get("/folders/999/", format="json")
    assert response.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_returns_empty_folder_list(api_client):
    """Ensure that if no folders were created yet we just get an empty list."""
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
def test_gets_document(api_client, document_1):
    pk = document_1.id
    response = api_client.get(f"/documents/{pk}/", format="json")
    assert response.status_code == 200

    document = response.data

    # Make sure deleted folder was excluded.
    assert document["title"] == "doc1"


@pytest.mark.django_db(transaction=True)
def test_fails_to_get_nonexistent_document(api_client):
    response = api_client.get("/documents/999/", format="json")
    assert response.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_fails_to_get_deleted_document(api_client, deleted_document):
    pk = deleted_document.id
    response = api_client.get(f"/documents/{pk}/", format="json")
    assert response.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_creates_document(api_client, parent_folder):
    document_data = {
        "title": "foobar ✓",
        "content": "quick brown dog",
        "folder": parent_folder.id,
    }
    response = api_client.post("/documents/", document_data, format="json")
    assert response.status_code == 201
    assert response.data["title"] == "foobar ✓"
    assert response.data["content"] == "quick brown dog"


@pytest.mark.django_db(transaction=True)
def test_fails_to_create_invalid_document(api_client, parent_folder):
    document_data = {
        "title": "foobar ✓",
        "folder": parent_folder.id,
    }
    response = api_client.post("/documents/", document_data, format="json")
    assert response.status_code == 400
    assert response.data["content"][0].code == "required"


@pytest.mark.django_db(transaction=True)
def test_move_document(api_client, document_1, child_folder):
    document_data = {"folder": child_folder.id}
    response = api_client.put(
        f"/documents/{document_1.id}/", document_data, format="json"
    )
    assert response.status_code == 200
    assert response.data["folder"] == child_folder.id

    updated_document = Document.objects.get(pk=response.data["id"])
    assert updated_document.folder.id == child_folder.id


@pytest.mark.django_db(transaction=True)
def test_tries_to_move_not_existing_document(api_client):
    document_data = {"title": "baz"}
    response = api_client.put("/documents/999/", document_data, format="json")

    assert response.status_code == 404


# ##########################
# ###   Topic API Tests  ###
# ##########################
@pytest.mark.django_db(transaction=True)
def test_gets_topic(api_client, topic_1):
    pk = topic_1.id
    response = api_client.get(f"/topics/{pk}/", format="json")
    assert response.status_code == 200

    topic = response.data

    # Make sure deleted folder was excluded.
    assert topic["name"] == "first topic"


@pytest.mark.django_db(transaction=True)
def test_gets_all_topics(api_client, topic_1, topic_2):
    response = api_client.get("/topics/", format="json")
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db(transaction=True)
def test_add_document_to_topic(api_client, document_1, topic_1, topic_2):
    response = api_client.post(
        f"/documents/{document_1.id}/topics/{topic_2.id}/", format="json"
    )
    assert response.status_code == 200
    assert response.data["topics"][1]["name"] == "second topic"

    updated_document = Document.objects.get(pk=response.data["id"])
    assert updated_document.topics.all()[1].name == "second topic"


@pytest.mark.django_db(transaction=True)
def test_remove_topic_from_document(api_client, document_1, topic_1, topic_2):
    response = api_client.delete(
        f"/documents/{document_1.id}/topics/{topic_2.id}/", format="json"
    )
    assert response.status_code == 200
    assert len(response.data["topics"]) == 1

    updated_document = Document.objects.get(pk=response.data["id"])
    assert len(updated_document.topics.all()) == 1


@pytest.mark.django_db(transaction=True)
def test_gets_docs_for_topic(api_client, topic_1, document_1):
    response = api_client.get(f"/topics/{topic_1.id}/documents/", format="json")
    assert response.status_code == 200
    assert response.data[0]["title"] == "doc1"


@pytest.mark.django_db(transaction=True)
def test_gets_docs_for_folder(api_client, parent_folder, document_1):
    response = api_client.get(f"/folders/{parent_folder.id}/documents/", format="json")
    assert response.status_code == 200
    assert response.data[0]["title"] == "doc1"
