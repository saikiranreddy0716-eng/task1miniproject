"""Functions for managing contacts."""

from typing import TypedDict


class Contact(TypedDict):
    id: str
    name: str
    phone: str


def search_contact(
    contacts: list[Contact], contact_id: str
) -> Contact | None:
    """Return a contact by ID, or None if it does not exist."""
    contact_id = contact_id.strip()

    for contact in contacts:
        if contact["id"] == contact_id:
            return contact

    return None


def create_contact(
    contacts: list[Contact], contact_id: str, name: str, phone: str
) -> Contact:
    """Create a contact after validating the input."""
    contact_id = contact_id.strip()
    name = name.strip()
    phone = phone.strip()

    if not contact_id or not name or not phone:
        raise ValueError("ID, name, and phone cannot be empty.")

    if search_contact(contacts, contact_id) is not None:
        raise ValueError(f"Contact ID '{contact_id}' already exists.")

    contact: Contact = {
        "id": contact_id,
        "name": name,
        "phone": phone,
    }
    contacts.append(contact)
    return contact


def list_contacts(contacts: list[Contact]) -> list[Contact]:
    """Return a copy of the contact list."""
    return contacts.copy()


def update_contact(
    contacts: list[Contact],
    contact_id: str,
    name: str,
    phone: str,
) -> Contact:
    """Update an existing contact."""
    contact_id = contact_id.strip()
    name = name.strip()
    phone = phone.strip()

    if not contact_id or not name or not phone:
        raise ValueError("ID, name, and phone cannot be empty.")

    contact = search_contact(contacts, contact_id)

    if contact is None:
        raise ValueError(f"Contact ID '{contact_id}' was not found.")

    contact["name"] = name
    contact["phone"] = phone
    return contact


def delete_contact(
    contacts: list[Contact], contact_id: str
) -> Contact:
    """Delete an existing contact."""
    contact_id = contact_id.strip()

    if not contact_id:
        raise ValueError("Contact ID cannot be empty.")

    contact = search_contact(contacts, contact_id)

    if contact is None:
        raise ValueError(f"Contact ID '{contact_id}' was not found.")

    contacts.remove(contact)
    return contact