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

    git clone <https://github.com/patilect/notes_app.git>

2. Navigate to the project directory:
    cd neofi_notes

3. Install dependencies
    pip install -r requirements.txt

4. Apply migrations
    python manage.py makemigrations
    python manage.py migrate

5. Run the development server:
    python manage.py runserver

6. Access the application at <http://localhost:8000>

## Testing

The project includes unit tests for the API endpoints. To run the tests, use the following command:
python manage.py test

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

The base URL for all API endpoints is: https://notesapp-production-5400.up.railway.app/

### Authentication

All endpoints require authentication using Token-based authentication. You need to include the Authorization header in your requests with the value Token <your_token_here>.

## Endpoints

1. Create a User Account
    POST /api/signup/
Description
Create a new user account.

Request Body
username (string): The username for the new user.
email (string): The email address for the new user.
password (string): The password for the new user.
Example
json
Copy code
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
Response
Status Code: 201 CREATED
Response Body: None
2. User Login
Endpoint
bash
Copy code
POST /api/login/
Description
Authenticate a user and get an authentication token.

Request Body
email (string): The email address of the user.
password (string): The password of the user.
Example
json
Copy code
{
  "email": "test@example.com",
  "password": "password123"
}
Response
Status Code: 200 OK
Response Body:
json
Copy code
{
  "token": "<your_authentication_token_here>"
}
3. Create a Note
Endpoint
bash
Copy code
POST /api/notes/create/
Description
Create a new note.

Request Body
content (string): The content of the note.
Example
json
Copy code
{
  "content": "This is a new note."
}
Response
Status Code: 201 CREATED
Response Body:
json
Copy code
{
  "id": 1,
  "content": "This is a new note.",
  "created_at": "2024-02-15T12:00:00Z",
  "updated_at": "2024-02-15T12:00:00Z"
}
4. Retrieve a Note
Endpoint
bash
Copy code
GET /api/notes/{note_id}/
Description
Retrieve details of a specific note by its ID.

Parameters
note_id (integer): The ID of the note to retrieve.
Example
bash
Copy code
GET /api/notes/1/
Response
Status Code: 200 OK
Response Body:
json
Copy code
{
  "id": 1,
  "content": "This is a new note.",
  "created_at": "2024-02-15T12:00:00Z",
  "updated_at": "2024-02-15T12:00:00Z"
}
5. Share a Note
Endpoint
bash
Copy code
POST /api/notes/share/
Description
Share a note with other users.

Request Body
note_id (integer): The ID of the note to share.
user_ids (array of integers): The IDs of the users to share the note with.
Example
json
Copy code
{
  "note_id": 1,
  "user_ids": [2, 3]
}
Response
Status Code: 201 CREATED
Response Body: None
6. Update a Note
Endpoint
bash
Copy code
PUT /api/notes/{note_id}/
Description
Update the content of a note.

Parameters
note_id (integer): The ID of the note to update.
Request Body
content (string): The updated content of the note.
Example
json
Copy code
{
  "content": "This is the updated content of the note."
}
Response
Status Code: 200 OK
Response Body:
json
Copy code
{
  "id": 1,
  "content": "This is the updated content of the note.",
  "created_at": "2024-02-15T12:00:00Z",
  "updated_at": "2024-02-15T12:05:00Z"
}
7. Get Note Version History
Endpoint
bash
Copy code
GET /api/notes/version-history/{note_id}/
Description
Retrieve the version history of a note.

Parameters
note_id (integer): The ID of the note to get the version history for.
Example
bash
Copy code
GET /api/notes/version-history/1/
Response
Status Code: 200 OK
Response Body:
json
Copy code
[
  {
    "id": 1,
    "note": 1,
    "previous_content": "This is the previous content.",
    "edited_content": "This is the updated content.",
    "edited_by": 2,
    "edit_timestamp": "2024-02-15T12:05:00Z"
  },
  {
    "id": 2,
    "note": 1,
    "previous_content": "This is the updated content.",
    "edited_content": "This is the latest content.",
    "edited_by": 2,
    "edit_timestamp": "2024-02-15T12:10:00Z"
  }
]
Conclusion
This document provides a detailed overview of the Neofi Notes App API endpoints along with usage examples.