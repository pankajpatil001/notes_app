# Neofi Notes App

Neofi Notes App is a simple Django Rest Framework based application for taking and sharing notes. It provides RESTful APIs for basic CRUD operations on notes, user authentication, and note sharing functionality.

## Features

- User registration and authentication
- Create, read, update, and delete notes
- Share notes with other users
- View version history of notes

## Installation

To run the Neofi Notes App locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/patilect/notes_app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd notes_app
    ```

3. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations

    ```bash
    python manage.py makemigrations
    python manage.py migrate

5. Run the development server:

    ```bash
    python manage.py runserver

6. Access the application at <http://localhost:8000>

## Testing

The project includes unit tests for the API endpoints. To run the tests, use the following command:

```bash
    python manage.py test
```

## Usage

## API Endpoints

POST /signup: Create a new user account.

POST /login: Log in to an existing user account.

POST /notes/create/: Create a new note.

GET /notes/{id}: Retrieve a specific note by its ID.

DELETe /notes/{id}: Delete a specific note by its ID.

POST /notes/share/: Share a note with other users.

PUT /notes/{id}/: Update an existing note.

GET /notes/version-history/{id}: Get all the changes associated with a note.


# API Documentation and Usage Examples

## Introduction

This document provides comprehensive documentation for the Neofi Notes App API endpoints along with usage examples.

### Base URL

The base URL for all API endpoints is:
https://notesapp-production-5400.up.railway.app/

### Authentication

All endpoints require authentication using Token-based authentication. You need to include the Authorization header in your requests with the value Token <your_token_here>.

## Endpoints

### Create a User Account

#### Endpoint

POST /signup/

#### Description

Create a new user account.

#### Request Body

- username (string): The username for the new user.
- email (string): The email address for the new user.
- password (string): The password for the new user.
- confirm_password (string): The same password repeated again.

#### Example

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "confirm_password": "password123"
}
```

#### Response

- Status Code: 201 CREATED

#### Response Body

```json
{
    "message": "User signup successful."
}
```

### User Login

#### Endpoint

POST /login/

#### Description

Authenticate a user and get the authentication token.

#### Request Body

- email (string): The email address for the user.
- password (string): The password for the user.

#### Example

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

#### Response

- Status Code: 200 OK

#### Response Body:

```json
{
    "message": "User login successful.",
    "user": {
        "email": "test@example.com",
        "username": "password123"
    },
    "token": "fdf2ab85e6a55aae3b395bac4d435d69fcdd89e3"
}
```

### Create a Note

#### Endpoint

POST /notes/create/

#### Description

Create a new note

#### Request Body

- content (string): The content of the note.

#### Example

```json
{
  "content": "This is a sample note."
}
```

#### Response

- Status Code: 201 CREATED

#### Response Body:

```json
{
    "message": "Note creation successful.",
    "note_id": 3,
    "owner": {
        "email": "test@example.com",
        "username": "password123"
    }
}
```

### Retrieve a Note

#### Endpoint

GET /notes/{note-id}/

#### Description

Retrieve details of a specific note by its ID.

#### Parameters

- note-id (integer): The ID of the note to retrieve.

#### Example

```bash
GET /notes/3/
```

#### Response

- Status Code: 200 OK

#### Response Body:

```json
{
    "id": 3,
    "content": "This is a sample note.",
    "created_at": "2024-02-19T19:13:57.630430Z",
    "updated_at": "2024-02-19T19:13:57.630460Z"
}
```

### Share a Note

#### Endpoint

POST /notes/share/

#### Description

Share a note with other users.

#### Request Body

- note_id (integer): The ID of the note to share.
- user_ids (array of integers): The IDs of the users to share the note with.

#### Example

```json
{
  "note_id": 3,
  "user_ids": [1, 2]
}
```

#### Response

- Status Code: 200 OK

#### Response Body:

```json
{
    "message": "Note share successful."
}
```

### Update a Note

#### Endpoint

PUT /notes/{note-id}/

#### Description

Update the content of a note.

#### Parameters

- note-id (integer): The ID of the note to update.

#### Request Body

- content (string): The updated content of the note.

#### Example

```json
{
  "content": "This is a sample note. Written by Pankaj Patil."
}
```

#### Response

- Status Code: 200 OK

#### Response Body:

```json
{
    "message": "Note update successful.",
    "data": {
        "id": 3,
        "content": "This is a sample note. Written by Pankaj Patil.",
        "created_at": "2024-02-19T19:13:57.630430Z",
        "updated_at": "2024-02-19T19:24:56.668865Z"
    }
}
```

### Get Note Version History

#### Endpoint

GET /notes/version-history/{note-id}/

#### Description

Retrieve the version history of a note.

#### Parameters

- note-id (integer): The ID of the note to retrieve version history.

#### Request Body

- content (string): The updated content of the note.

#### Example

```bash
GET /notes/version-history/3/
```

#### Response

- Status Code: 200 OK

#### Response Body:

```json
[
    {
        "note": 3,
        "previous_content": "",
        "edited_content": "This is a sample note.",
        "edited_by": 4,
        "edit_timestamp": "2024-02-19T19:13:57.689300Z"
    },
    {
        "note": 3,
        "previous_content": "This is a sample note.",
        "edited_content": "This is a sample note. Written by Pankaj Patil.",
        "edited_by": 4,
        "edit_timestamp": "2024-02-19T19:24:56.698648Z"
    }
]
```

### Delete a note

#### Endpoint

Delete /notes/{note-id}/

#### Description

Delete a note and related items like note shares and note history.

#### Parameters

- note-id (integer): The ID of the note to delete.

#### Example

```bash
DELETE /notes/3/
```

#### Response

- Status Code: 204 NO CONTENT

#### Response Body:

```json
{
    "message": "Note deleted."
}
```

## Conclusion

This document provides a detailed overview of the Neofi Notes App API endpoints along with usage examples.
