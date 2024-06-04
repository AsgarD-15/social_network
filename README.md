# Social Network API

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

4. Run migrations:

    ```bash
    docker-compose run web python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    docker-compose run web python manage.py createsuperuser
    ```

## Endpoints

- `POST /api/login/`: Login with email and password.
- `GET /api/search/`: Search users by email or name.
- `POST /api/friend-request/`: Send a friend request.
- `POST /api/friend-request/accept/<id>/`: Accept a friend request.
- `POST /api/friend-request/reject/<id>/`: Reject a friend request.
- `GET /api/friends/`: List friends.
- `GET /api/pending-requests/`: List pending friend requests.
