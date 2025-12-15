# IPO Chart - Event Planner Application

## Overview
This document provides Input-Process-Output (IPO) charts for all major functions and modules in the Event Planner Application.

---

## 1. User Registration Module

### Function: `register()`

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| • Username (text) | 1. Validate input fields are not empty | • Success: Redirect to login page |
| • Email (text) | 2. Validate passwords match | • Flash message: "Registration successful!" |
| • Password (text) | 3. Hash password using Werkzeug | • Error: Stay on registration page |
| • Confirm Password (text) | 4. Execute SQL INSERT query | • Flash message: Error details |
| | 5. Handle duplicate username/email | • Database: New user record created |
| | 6. Commit to database | |

**SQL Query Used:**
```sql
INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)
```

---

## 2. User Login Module

### Function: `login()`

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| • Username (text) | 1. Validate input fields are not empty | • Success: Redirect to dashboard |
| • Password (text) | 2. Execute SQL SELECT query to find user | • Flash message: "Welcome back, {username}!" |
| | 3. Verify password hash matches | • Session: Set user_id and username |
| | 4. Create user session | • Error: Stay on login page |
| | 5. Store user_id in session | • Flash message: "Invalid credentials" |

**SQL Query Used:**
```sql
SELECT * FROM users WHERE username = ?
```

---

## 3. User Logout Module

### Function: `logout()`

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| • Current session data | 1. Clear all session data | • Redirect to home page |
| | 2. Remove user_id from session | • Flash message: "You have been logged out" |
| | | • Session: Cleared |

---

## 4. Dashboard Module

### Function: `dashboard()`

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| • User session (user_id) | 1. Check if user is logged in | • Success: Render dashboard.html |
| | 2. Execute SQL SELECT query for events | • List of user's events |
| | 3. Order events by due_date | • Event data: title, description, location, due_date, status |
| | 4. Fetch all events for current user | • Error: Redirect to login |
| | 5. Pass events to template | |

**SQL Query Used:**
```sql
SELECT * FROM events WHERE user_id = ? ORDER BY due_date ASC
```

---

## 5. Create Event Module

### Function: `create_event()`

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| • Title (text) | 1. Check user is logged in | • Success: Redirect to dashboard |
| • Description (text, optional) | 2. Validate required fields (title, due_date) | • Flash message: "Event created successfully!" |
| • Location (text, optional) | 3. Get user_id from session | • Database: New event record created |
| • Due Date (datetime) | 4. Execute SQL INSERT query | • Error: Stay on create page |
| • Status (dropdown) | 5. Commit to database | • Flash message: Error details |

**SQL Query Used:**
```sql
INSERT INTO events (user_id, title, description, location, due_date, status)
VALUES (?, ?, ?, ?, ?, ?)
```

---

## 6. Edit Event Module

### Function: `edit_event(event_id)`

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| • Event ID (integer) | **GET Request:** | • Success: Render edit_event.html |
| • Title (text) | 1. Check user is logged in | • Pre-filled form with event data |
| • Description (text, optional) | 2. Execute SQL SELECT query | • Error: Redirect to dashboard |
| • Location (text, optional) | 3. Verify event belongs to user | • Flash message: Error details |
| • Due Date (datetime) | 4. Pass event data to template | |
| • Status (dropdown) | **POST Request:** | • Success: Redirect to dashboard |
| | 5. Validate required fields | • Flash message: "Event updated!" |
| | 6. Execute SQL UPDATE query | • Database: Event record updated |
| | 7. Update updated_at timestamp | |

**SQL Queries Used:**
```sql
-- GET: Fetch event
SELECT * FROM events WHERE id = ? AND user_id = ?

-- POST: Update event
UPDATE events 
SET title = ?, description = ?, location = ?, due_date = ?, status = ?, 
    updated_at = CURRENT_TIMESTAMP
WHERE id = ? AND user_id = ?
```

---

## 7. Delete Event Module

### Function: `delete_event(event_id)`

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| • Event ID (integer) | 1. Check user is logged in | • Success: Redirect to dashboard |
| • User session (user_id) | 2. Verify event belongs to user | • Flash message: "Event deleted successfully!" |
| | 3. Execute SQL DELETE query | • Database: Event record removed |
| | 4. Commit to database | |

**SQL Query Used:**
```sql
DELETE FROM events WHERE id = ? AND user_id = ?
```

---

## 8. Database Initialization Module

### Function: `init_db()`

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| • None (runs automatically) | 1. Connect to SQLite database | • Database file created |
| | 2. Check if tables exist | • Users table created |
| | 3. Create users table if not exists | • Events table created |
| | 4. Create events table if not exists | • Console: "Database initialized successfully!" |
| | 5. Commit changes | |

**SQL Queries Used:**
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    location TEXT,
    due_date TIMESTAMP NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
)
```

---

## 9. Database Connection Module

### Function: `get_db_connection()`

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| • None | 1. Create SQLite connection | • Database connection object |
| | 2. Set row_factory to sqlite3.Row | • Rows accessible as dictionaries |
| | 3. Return connection object | |

---

## System-Level IPO Chart

### Overall Application Flow

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| **User Actions:** | **Application Processing:** | **User Experience:** |
| • HTTP requests | 1. Flask routes incoming requests | • HTML pages rendered |
| • Form submissions | 2. Check authentication/authorization | • User data displayed |
| • Login credentials | 3. Execute business logic | • Success/error messages |
| • Event data | 4. Interact with SQLite database | • Redirects to appropriate pages |
| | 5. Use vanilla SQL (no ORM) | • Session management |
| | 6. Render HTML templates | • Secure authentication |
| | 7. Return HTTP responses | |

---

## Data Flow Diagram

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       │ HTTP Request
       │
       ▼
┌─────────────────┐
│  Flask App      │
│  (app.py)       │
└────────┬────────┘
         │
         │ Function Calls
         │
         ▼
┌─────────────────┐
│  Database       │
│  Module         │
│  (database.py)  │
└────────┬────────┘
         │
         │ SQL Queries
         │
         ▼
┌─────────────────┐
│  SQLite DB      │
│ (eventplanner.db)│
└─────────────────┘
```

---

## Security Processing

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| • Plain text password | 1. Hash using Werkzeug scrypt | • Hashed password stored |
| • User credentials | 2. Verify hash on login | • Session cookie created |
| • SQL parameters | 3. Use parameterized queries | • SQL injection prevented |
| • Session data | 4. Validate on each request | • Unauthorized access blocked |

---

## Error Handling Flow

| INPUT | PROCESS | OUTPUT |
|-------|---------|--------|
| • Invalid data | 1. Validate input | • Flash error message |
| • Database errors | 2. Catch exceptions | • User-friendly error display |
| • Authentication failures | 3. Log errors | • Redirect to appropriate page |
| • Missing required fields | 4. Return appropriate response | • Form validation feedback |

---

## Version History

| Version | Date       | Changes                     |
|---------|------------|-----------------------------|
| 1.0     | 2025-12-15 | Initial IPO chart creation  |
