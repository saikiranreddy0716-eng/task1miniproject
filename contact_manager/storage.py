"""Save and load contacts using JSON files."""

import json
import os
from pathlib import Path
from typing import Any

from contact_manager.operations import Contact


def validate_contacts(data: Any) -> list[Contact]:
    """Validate data read from a JSON file."""
    if not isinstance(data, list):
        raise ValueError("JSON must contain a list of contacts.")

    contacts: list[Contact] = []
    seen_ids: set[str] = set()

    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each contact must be a JSON object.")

        if set(item) != {"id", "name", "phone"}:
            raise ValueError("Each contact must have id, name, and phone.")

        contact_id = item["id"]
        name = item["name"]
        phone = item["phone"]

        for label, value in (
            ("ID", contact_id),
            ("name", name),
            ("phone", phone),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Contact {label} cannot be empty.")

            if value != value.strip():
                raise ValueError(f"Contact {label} has extra outer spaces.")

        if contact_id in seen_ids:
            raise ValueError(f"Duplicate contact ID '{contact_id}'.")

        seen_ids.add(contact_id)
        contacts.append({
            "id": contact_id,
            "name": name,
            "phone": phone,
        })

    return contacts


def load_contacts(file_path: str | Path) -> list[Contact]:
    """Load contacts. Return an empty list if the file is missing."""
    path = Path(file_path)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in '{path}'. The file was not changed."
        ) from error

    return validate_contacts(data)


def save_contacts(
    file_path: str | Path, contacts: list[Contact]
) -> None:
    """Validate and safely save contacts to a JSON file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    validated = validate_contacts(contacts)

    # Do not overwrite a file that already contains invalid JSON.
    if path.exists():
        load_contacts(path)

    temporary_path = path.with_name(path.name + ".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(validated, file, indent=2, ensure_ascii=False)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        # Replace the original file only after the temporary file is written.
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()