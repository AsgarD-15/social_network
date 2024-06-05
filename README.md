# Social Network API

## Installation

1. Make sure the docker is installed in local computer.
2. Clone the repository
3. Navigate to the project directory
4. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```
5. Use the below Url:
   
    ```bash
    http://127.0.0.1:8000/
    ```
## Endpoints

- `POST /api/login/`: Login with email and password.
- `GET /api/search/`: Search users by email or name.
- `POST /api/friend-request/`: Send a friend request.
- `POST /api/friend-request/accept/<id>/`: Accept a friend request.
- `POST /api/friend-request/reject/<id>/`: Reject a friend request.
- `GET /api/friends/`: List friends.
- `GET /api/pending-requests/`: List pending friend requests.

Example Testcases.
Sign Up
Request:
POST /api/signup/
Content-Type: application/json

{
    "username": "testuser1",
    "email": "testuser1@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User1"
}


Request:
POST /api/signup/
Content-Type: application/json

{
    "username": "testuser2",
    "email": "testuser2@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User2"
}

Log In
Request:
POST /api/login/
Content-Type: application/json

{
    "username": "testuser1",
    "password": "password123"
}


Send Friend Request
Request:
POST /api/friend-request/
Content-Type: application/json
Authorization: Token your_api_token

{
    "receiver_id": 2
}


List Friends
Request:
GET /api/friends/
Authorization: Token your_api_token


Accept Friend Request
Request:
POST /api/friend-request/accept/1/
Authorization: Token your_api_token

List Pending Friend Requests
Request:
GET /api/pending-requests/
Authorization: Token your_api_token
