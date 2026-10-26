import pytest

from contact_manager.operations import (
    create_contact,
    delete_contact,
    list_contacts,
    search_contact,
    update_contact,
)


@pytest.fixture
def contacts():
    return []


def test_create_contact(contacts):
    create_contact(contacts, "101", "Ravi", "9876543210")
    assert contacts[0]["name"] == "Ravi"


def test_create_rejects_empty_fields(contacts):
    with pytest.raises(ValueError):
        create_contact(contacts, "", "Ravi", "9876543210")


def test_duplicate_id_is_rejected(contacts):
    create_contact(contacts, "101", "Ravi", "9876543210")

    with pytest.raises(ValueError, match="already exists"):
        create_contact(contacts, "101", "Priya", "9876543211")


def test_list_empty_contacts(contacts):
    assert list_contacts(contacts) == []


def test_search_missing_contact(contacts):
    assert search_contact(contacts, "999") is None


def test_search_existing_contact(contacts):
    create_contact(contacts, "101", "Ravi", "9876543210")
    assert search_contact(contacts, "101")["name"] == "Ravi"


def test_update_contact(contacts):
    create_contact(contacts, "101", "Ravi", "9876543210")
    update_contact(contacts, "101", "Ravi Kumar", "9876543211")

    assert contacts[0]["name"] == "Ravi Kumar"
    assert contacts[0]["phone"] == "9876543211"


def test_update_missing_contact(contacts):
    with pytest.raises(ValueError, match="was not found"):
        update_contact(contacts, "999", "Ravi", "9876543210")


def test_delete_contact(contacts):
    create_contact(contacts, "101", "Ravi", "9876543210")
    delete_contact(contacts, "101")

    assert contacts == []


def test_delete_missing_contact(contacts):
    with pytest.raises(ValueError, match="was not found"):
        delete_contact(contacts, "999")