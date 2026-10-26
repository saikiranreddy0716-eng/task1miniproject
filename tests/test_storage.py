import json

import pytest

from contact_manager.storage import load_contacts, save_contacts


def test_missing_file_returns_empty_list(tmp_path):
    path = tmp_path / "contacts.json"

    assert load_contacts(path) == []
    assert not path.exists()


def test_save_and_load_contacts(tmp_path):
    path = tmp_path / "contacts.json"
    records = [
        {"id": "101", "name": "Ravi", "phone": "9876543210"}
    ]

    save_contacts(path, records)
    assert load_contacts(path) == records


def test_malformed_json_is_rejected(tmp_path):
    path = tmp_path / "contacts.json"
    path.write_text("{broken JSON", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_contacts(path)


def test_corrupt_file_is_not_overwritten(tmp_path):
    path = tmp_path / "contacts.json"
    original = "{broken JSON"
    path.write_text(original, encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        save_contacts(
            path,
            [{"id": "101", "name": "Ravi", "phone": "9876543210"}],
        )

    assert path.read_text(encoding="utf-8") == original


def test_wrong_json_structure_is_rejected(tmp_path):
    path = tmp_path / "contacts.json"
    path.write_text(
        '{"id":"101","name":"Ravi","phone":"9876543210"}',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="list of contacts"):
        load_contacts(path)


def test_duplicate_ids_in_json_are_rejected(tmp_path):
    path = tmp_path / "contacts.json"
    records = [
        {"id": "101", "name": "Ravi", "phone": "9876543210"},
        {"id": "101", "name": "Priya", "phone": "9876543211"},
    ]
    path.write_text(json.dumps(records), encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate contact ID"):
        load_contacts(path)


def test_invalid_data_does_not_replace_existing_file(tmp_path):
    path = tmp_path / "contacts.json"
    original = json.dumps([
        {"id": "101", "name": "Ravi", "phone": "9876543210"}
    ])
    path.write_text(original, encoding="utf-8")

    with pytest.raises(ValueError):
        save_contacts(
            path,
            [{"id": "", "name": "Ravi", "phone": "9876543210"}],
        )

    assert path.read_text(encoding="utf-8") == original