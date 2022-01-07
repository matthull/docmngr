import pytest

from rest_framework.test import APIClient

from docmngr.models import Document, Folder


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def parent_folder(transactional_db):
    folder = Folder(name="top_1")
    folder.save()

    return folder


@pytest.fixture
def child_folder(transactional_db, parent_folder):
    # Include a unicode character in name to make sure we're testing unicode support
    folder = Folder(name="child_1 ✓", parent_folder=parent_folder)
    folder.save()

    return folder


@pytest.fixture
def deleted_folder(transactional_db, parent_folder):
    folder = Folder(name="child_2", parent_folder=parent_folder, is_deleted=True)
    folder.save()

    return folder


@pytest.fixture
def document_1(transactional_db, parent_folder):
    document = Document(title="doc1", folder=parent_folder)
    document.save()

    return document


@pytest.fixture
def deleted_document(transactional_db, parent_folder):
    document = Document(title="byebye", folder=parent_folder, is_deleted=True)
    document.save()

    return document
