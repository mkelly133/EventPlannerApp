# Event Planner App

A simple, interactive web application for managing events with user authentication. Built with Flask and SQLite3 using vanilla SQL (no ORM).

## Features

- 🔐 **User Authentication**: Secure registration and login system with password hashing
- 📅 **Event Management**: Create, read, update, and delete events
- ⏰ **Due Dates**: Track event deadlines and schedules
- 📍 **Location Tracking**: Add locations to your events
- ✅ **Status Tracking**: Monitor event status (pending, in-progress, completed)
- 📊 **Dashboard**: View all your events in an organized layout
- 🎨 **Responsive Design**: Modern, mobile-friendly user interface

## Technology Stack

- **Backend**: Flask 2.3.2
- **Database**: SQLite3 (vanilla SQL, no ORM)
- **Password Security**: Werkzeug 2.3.6
- **Frontend**: HTML5, CSS3

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository** (if not already cloned):
   ```bash
   git clone <repository-url>
   cd EventPlannerApp
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**:
   The database is automatically initialized when you first run the application.
   Alternatively, you can manually initialize it:
   ```bash
   python database.py
   ```

4. **Run the application**:
   ```bash
   flask --debug run
   ```
   Or using Python directly:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage Guide

### Getting Started

1. **Register a New Account**:
   - Click "Register" on the home page
   - Enter a unique username and email
   - Create a secure password
   - Confirm your password
   - Click "Register"

2. **Login**:
   - Enter your username and password
   - Click "Login"
   - You'll be redirected to your dashboard

3. **Create Your First Event**:
   - From the dashboard, click "+ Create New Event"
   - Fill in the event details:
     - **Title** (required): Name of your event
     - **Description** (optional): Detailed information about the event
     - **Location** (optional): Where the event will take place
     - **Due Date** (required): When the event is scheduled
     - **Status**: Select pending, in-progress, or completed
   - Click "Create Event"

4. **Manage Events**:
   - **View Events**: All your events are displayed on the dashboard
   - **Edit Event**: Click the "Edit" button on any event card
   - **Delete Event**: Click the "Delete" button and confirm deletion
   - **Status Color Coding**:
     - 🟡 Yellow: Pending events
     - 🔵 Blue: In-progress events
     - 🟢 Green: Completed events

5. **Logout**:
   - Click "Logout" in the navigation bar when you're done

## Database Schema

The application uses two main tables:

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Securely hashed password
- `email`: User's email address
- `created_at`: Account creation timestamp

### Events Table
- `id`: Primary key
- `user_id`: Foreign key referencing users table
- `title`: Event name
- `description`: Event details
- `location`: Event location
- `due_date`: Event due date/time
- `status`: Event status (pending/in-progress/completed)
- `created_at`: Event creation timestamp
- `updated_at`: Last update timestamp

For detailed database information, see [DATA_DICTIONARY.md](DATA_DICTIONARY.md)

## Documentation

- **[Data Dictionary](DATA_DICTIONARY.md)**: Comprehensive database schema documentation
- **[IPO Chart](IPO_CHART.md)**: Input-Process-Output documentation for all modules

## Security Features

- ✅ **Password Hashing**: Uses Werkzeug's secure password hashing (scrypt algorithm)
- ✅ **SQL Injection Prevention**: All queries use parameterized statements
- ✅ **Session Management**: Secure session handling with Flask sessions
- ✅ **Authentication Required**: Protected routes require user login
- ✅ **User Data Isolation**: Users can only access their own events

## Project Structure

```
EventPlannerApp/
├── app.py                  # Main Flask application
├── database.py             # Database initialization and connection
├── requirements.txt        # Python dependencies
├── DATA_DICTIONARY.md      # Database documentation
├── IPO_CHART.md           # IPO chart documentation
├── README.md              # This file
├── eventplanner.db        # SQLite database (auto-generated)
├── static/
│   ├── main.css           # Application styles
│   └── Octocat.png        # Logo image
└── templates/
    ├── index.html         # Home page
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── dashboard.html     # User dashboard
    ├── create_event.html  # Event creation form
    └── edit_event.html    # Event edit form
```

## Development

### Running in Debug Mode

```bash
flask --debug run
```

Debug mode enables:
- Auto-reload on code changes
- Detailed error messages
- Debug toolbar

### Database Management

**Initialize/Reset Database**:
```python
from database import init_db, drop_tables

# Drop all tables and recreate them
drop_tables()
init_db()
```

**View Database**:
You can use any SQLite browser or command-line tool:
```bash
sqlite3 eventplanner.db
```

## API Routes

| Route | Method | Description | Auth Required |
|-------|--------|-------------|---------------|
| `/` | GET | Home page | No |
| `/register` | GET, POST | User registration | No |
| `/login` | GET, POST | User login | No |
| `/logout` | GET | User logout | Yes |
| `/dashboard` | GET | User dashboard | Yes |
| `/event/create` | GET, POST | Create new event | Yes |
| `/event/<id>/edit` | GET, POST | Edit event | Yes |
| `/event/<id>/delete` | POST | Delete event | Yes |

## Troubleshooting

**Issue**: Database file not found
- **Solution**: Run `python database.py` to initialize the database

**Issue**: Password hash errors
- **Solution**: Ensure Werkzeug is installed: `pip install Werkzeug==2.3.6`

**Issue**: Port already in use
- **Solution**: Use a different port: `flask run --port 5001`

**Issue**: Session not persisting
- **Solution**: Ensure `SECRET_KEY` is set in environment or app.py

## Contributing

This is a simple educational project demonstrating:
- Flask web development
- User authentication
- Database management with vanilla SQL
- CRUD operations
- Documentation best practices

## License

This project is created for educational purposes.

## Version History

- **v1.0** (2025-12-15): Initial release
  - User authentication system
  - Event CRUD operations
  - Dashboard interface
  - Complete documentation

## Contact

For questions or issues, please create an issue in the repository.

---

Built with Flask and ❤️
