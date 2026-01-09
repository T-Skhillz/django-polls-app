# Polls API

A Django REST Framework-based polling application that allows users to create questions, add choices, and vote on polls.

## Features

- **User Authentication**: JWT-based authentication with token refresh
- **Question Management**: Create and manage poll questions
- **Multiple Choice Options**: Add multiple choices to each question
- **Voting System**: Users can vote on polls with one vote per question constraint
- **Results Endpoint**: View aggregated voting results for each question
- **Admin Interface**: Nested admin interface for managing questions, choices, and votes

## Tech Stack

- **Django 5.2**
- **Django REST Framework**: API endpoints
- **PostgreSQL**: Database
- **JWT Authentication**: Simple JWT for token-based auth
- **Django Nested Admin**: Enhanced admin interface

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   
   # Local Development Database
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # Production Database (Render)
   DATABASE_URL=your-production-database-url
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Seed the database (optional)**
   ```bash
   python manage.py seed_data
   ```
   This creates a test user (`tester`/`password123`) and sample poll questions.

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

- **POST** `/api/auth/login/` - Obtain JWT access and refresh tokens
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

- **POST** `/api/auth/refresh/` - Refresh access token
  ```json
  {
    "refresh": "your_refresh_token"
  }
  ```

### Questions

- **GET** `/api/v1/questions/` - List all questions
- **POST** `/api/v1/questions/` - Create a new question
- **GET** `/api/v1/questions/{id}/` - Retrieve a specific question
- **PUT/PATCH** `/api/v1/questions/{id}/` - Update a question
- **DELETE** `/api/v1/questions/{id}/` - Delete a question
- **GET** `/api/v1/questions/{id}/results/` - Get voting results for a question

### Choices

- **GET** `/api/v1/choices/` - List all choices
- **POST** `/api/v1/choices/` - Create a new choice
- **GET** `/api/v1/choices/{id}/` - Retrieve a specific choice
- **PUT/PATCH** `/api/v1/choices/{id}/` - Update a choice
- **DELETE** `/api/v1/choices/{id}/` - Delete a choice

### Votes

- **GET** `/api/v1/votes/` - List current user's votes
- **POST** `/api/v1/votes/` - Cast a vote
  ```json
  {
    "choice": choice_id
  }
  ```
- **GET** `/api/v1/votes/{id}/` - Retrieve a specific vote
- **PUT/PATCH** `/api/v1/votes/{id}/` - Update a vote
- **DELETE** `/api/v1/votes/{id}/` - Delete a vote

## Authentication

All API endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

**Token Lifetime:**
- Access Token: 1 day
- Refresh Token: 7 days

## Data Models

### Question
- `title`: Poll question text
- `user`: Question creator (ForeignKey to User)
- `published_at`: Timestamp of creation
- `completed`: Boolean flag for poll status

### Choice
- `question`: Related question (ForeignKey)
- `choice_text`: Choice option text

### Vote
- `user`: User who voted (ForeignKey)
- `question`: Related question (ForeignKey, auto-populated)
- `choice`: Selected choice (ForeignKey)
- `created_at`: Timestamp of vote

**Constraints:**
- Users can only vote once per question (enforced via unique constraint and validation)

## Admin Interface

Access the admin interface at `/admin/` with superuser credentials.

Features:
- Nested inline editing for questions, choices, and votes
- Vote count annotations
- Filtering by completion status, publish date, and user
- Search functionality

## Permissions

- **IsOwnerOrAuthenticated**: Custom permission allowing:
  - Authenticated users to view resources
  - Only resource owners to modify/delete their resources

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Shell Access
```bash
python manage.py shell_plus  # Requires django-extensions
```

## Deployment

The application is configured for deployment on Render with PostgreSQL. Ensure the `DATABASE_URL` environment variable is set in production.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate tests.