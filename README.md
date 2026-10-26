# Contact Manager CLI

A beginner-friendly Python command-line application to create, list,
search, update, and delete contacts.

## Features

- Create contacts with unique IDs
- List all contacts
- Search by contact ID
- Update existing contacts
- Delete existing contacts
- Validate empty and duplicate records
- Store contacts in a JSON file
- Handle missing and malformed JSON files
- Automated tests using pytest

## Requirements

- Python 3.10 or newer
- pip
- Git
- pytest for running tests

## Setup on Windows PowerShell

Open a terminal in the project directory.

Create a virtual environment:

    python -m venv .venv

Activate it:

    .\.venv\Scripts\Activate.ps1

Install the test dependency:

    python -m pip install pytest

## Run the application

    python -m contact_manager.cli

## Run tests

    python -m pytest -v

Tests use temporary files and do not require network services.

## Data storage

Contacts are saved in contacts.json in the project root.
The file is created when the first contact is saved.

The local contacts.json file is excluded from Git.

## Project structure

    task1miniproject/
    ├── contact_manager/
    │   ├── __init__.py
    │   ├── operations.py
    │   ├── storage.py
    │   └── cli.py
    ├── tests/
    │   ├── test_operations.py
    │   └── test_storage.py
    ├── .gitignore
    └── README.md

## Known limitations

- Contact IDs must be unique.
- Phone numbers are stored as text; advanced phone-number validation
  is not implemented.
- The application is intended for local, single-user use.
- There is no encryption or multi-user access control.
- The JSON file should be backed up if its contents are important.

## Error handling

- Empty values are rejected.
- Duplicate contact IDs are rejected.
- Missing records produce an error message.
- Missing JSON files are treated as an empty contact list.
- Malformed JSON is reported instead of silently overwritten.

## Privacy

Do not commit contacts.json because it may contain personal information.