"""Menu-driven Contact Manager command-line application."""

from pathlib import Path

from contact_manager.operations import (
    Contact,
    create_contact,
    delete_contact,
    list_contacts,
    search_contact,
    update_contact,
)
from contact_manager.storage import load_contacts, save_contacts


DATA_FILE = Path(__file__).resolve().parent.parent / "contacts.json"


def show_menu() -> None:
    """Display the main menu."""
    print("\n===== Contact Manager =====")
    print("1. Create contact")
    print("2. List contacts")
    print("3. Search contact")
    print("4. Update contact")
    print("5. Delete contact")
    print("6. Exit")


def main() -> None:
    """Run the Contact Manager."""
    try:
        contacts: list[Contact] = load_contacts(DATA_FILE)
    except (ValueError, OSError) as error:
        print(f"Could not load contacts: {error}")
        print("Inspect or repair contacts.json before continuing.")
        return

    print(f"Data file: {DATA_FILE}")

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        try:
            if choice == "1":
                updated = [dict(item) for item in contacts]

                contact = create_contact(
                    updated,
                    input("Enter contact ID: "),
                    input("Enter name: "),
                    input("Enter phone number: "),
                )

                save_contacts(DATA_FILE, updated)
                contacts[:] = updated
                print(f"Created contact: {contact['name']}")

            elif choice == "2":
                records = list_contacts(contacts)

                if not records:
                    print("No contacts found.")
                else:
                    for item in records:
                        print(
                            f"ID: {item['id']} | Name: {item['name']} "
                            f"| Phone: {item['phone']}"
                        )

            elif choice == "3":
                contact_id = input("Enter contact ID: ")
                contact = search_contact(contacts, contact_id)

                if contact is None:
                    print("Contact not found.")
                else:
                    print(contact)

            elif choice == "4":
                contact_id = input("Enter contact ID to update: ")
                name = input("Enter new name: ")
                phone = input("Enter new phone number: ")

                updated = [dict(item) for item in contacts]
                update_contact(updated, contact_id, name, phone)

                save_contacts(DATA_FILE, updated)
                contacts[:] = updated
                print("Contact updated successfully.")

            elif choice == "5":
                contact_id = input("Enter contact ID to delete: ")
                contact = search_contact(contacts, contact_id)

                if contact is None:
                    raise ValueError(
                        f"Contact ID '{contact_id.strip()}' was not found."
                    )

                remaining = [
                    item for item in contacts
                    if item["id"] != contact["id"]
                ]

                save_contacts(DATA_FILE, remaining)
                contacts[:] = remaining
                print("Contact deleted successfully.")

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Enter a number from 1 to 6.")

        except ValueError as error:
            print(f"Error: {error}")
        except OSError as error:
            print(f"File error: {error}")


if __name__ == "__main__":
    main()