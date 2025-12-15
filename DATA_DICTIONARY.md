# Data Dictionary - Event Planner Application

## Overview
This document provides a comprehensive description of all database tables, fields, and their relationships in the Event Planner Application.

## Database: eventplanner.db
**Database Type:** SQLite3  
**Location:** Root directory of the application

---

## Table: users

**Description:** Stores user account information for authentication and authorization.

| Column Name    | Data Type | Constraints              | Description                                      |
|---------------|-----------|--------------------------|--------------------------------------------------|
| id            | INTEGER   | PRIMARY KEY AUTOINCREMENT| Unique identifier for each user                  |
| username      | TEXT      | UNIQUE NOT NULL          | User's login username (must be unique)           |
| password_hash | TEXT      | NOT NULL                 | Hashed password using Werkzeug's password hasher |
| email         | TEXT      | UNIQUE NOT NULL          | User's email address (must be unique)            |
| created_at    | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP| Timestamp when the user account was created      |

**Indexes:**
- Primary Key on `id`
- Unique constraint on `username`
- Unique constraint on `email`

**Sample Data:**
```sql
id: 1
username: 'john_doe'
password_hash: 'scrypt:32768:8:1$...'
email: 'john@example.com'
created_at: '2025-12-15 10:30:00'
```

---

## Table: events

**Description:** Stores event information created by users, including event details, dates, and status.

| Column Name  | Data Type | Constraints                    | Description                                           |
|-------------|-----------|--------------------------------|-------------------------------------------------------|
| id          | INTEGER   | PRIMARY KEY AUTOINCREMENT      | Unique identifier for each event                      |
| user_id     | INTEGER   | NOT NULL, FOREIGN KEY (users.id)| Reference to the user who created the event          |
| title       | TEXT      | NOT NULL                       | Event title/name                                      |
| description | TEXT      | NULL                           | Detailed description of the event                     |
| location    | TEXT      | NULL                           | Location where the event will take place              |
| due_date    | TIMESTAMP | NOT NULL                       | Date and time when the event is due/scheduled         |
| status      | TEXT      | DEFAULT 'pending'              | Current status: 'pending', 'in-progress', 'completed' |
| created_at  | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP      | Timestamp when the event was created                  |
| updated_at  | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP      | Timestamp when the event was last updated             |

**Indexes:**
- Primary Key on `id`
- Foreign Key on `user_id` referencing `users(id)` with CASCADE DELETE

**Foreign Key Relationships:**
- `user_id` → `users.id` (ON DELETE CASCADE): When a user is deleted, all their events are also deleted

**Valid Status Values:**
- `pending`: Event has not started yet
- `in-progress`: Event is currently ongoing
- `completed`: Event has been completed

**Sample Data:**
```sql
id: 1
user_id: 1
title: 'Team Meeting'
description: 'Monthly team sync to discuss project updates'
location: 'Conference Room A'
due_date: '2025-12-20 14:00:00'
status: 'pending'
created_at: '2025-12-15 10:35:00'
updated_at: '2025-12-15 10:35:00'
```

---

## Relationships

### One-to-Many: users → events
- **Type:** One user can have many events
- **Relationship:** One-to-Many (1:N)
- **Implementation:** `events.user_id` references `users.id`
- **Cascade Rule:** DELETE CASCADE (deleting a user deletes all their events)

**ER Diagram:**
```
┌─────────────┐         ┌─────────────┐
│   users     │         │   events    │
├─────────────┤         ├─────────────┤
│ id (PK)     │────────<│ id (PK)     │
│ username    │    1:N  │ user_id (FK)│
│ password_hash│         │ title       │
│ email       │         │ description │
│ created_at  │         │ location    │
└─────────────┘         │ due_date    │
                        │ status      │
                        │ created_at  │
                        │ updated_at  │
                        └─────────────┘
```

---

## Data Validation Rules

### Users Table
1. **username**: Must be unique, cannot be empty
2. **email**: Must be unique, must be valid email format, cannot be empty
3. **password**: Minimum 1 character (application level), hashed before storage

### Events Table
1. **title**: Cannot be empty
2. **due_date**: Must be a valid datetime, cannot be empty
3. **status**: Must be one of: 'pending', 'in-progress', 'completed'
4. **user_id**: Must reference an existing user

---

## Security Considerations

1. **Password Storage**: Passwords are never stored in plain text. They are hashed using Werkzeug's `generate_password_hash()` function with scrypt algorithm.

2. **SQL Injection Prevention**: All database queries use parameterized statements (? placeholders) to prevent SQL injection attacks.

3. **Session Management**: User sessions are managed securely using Flask's session management with secret keys.

4. **Data Integrity**: Foreign key constraints ensure referential integrity between users and events.

---

## Database Initialization

The database is automatically initialized when the application starts. The initialization script (`database.py`) creates tables if they don't exist.

**Initialization Command:**
```python
from database import init_db
init_db()
```

---

## Backup and Maintenance

**Backup:** Since SQLite stores data in a single file (`eventplanner.db`), backing up is as simple as copying the database file.

**Location:** `/EventPlannerApp/eventplanner.db`

**Recommended Backup Strategy:**
- Daily automated backups of the database file
- Keep multiple versions for disaster recovery

---

## Version History

| Version | Date       | Changes                          |
|---------|------------|----------------------------------|
| 1.0     | 2025-12-15 | Initial database schema creation |
