# TaskFlow - Task Management Application

TaskFlow is a full-stack task management web application developed using Python Flask and MySQL.

## Features

- User registration
- Secure login and logout
- Password hashing
- User authentication and authorization
- Create tasks
- View tasks
- Edit tasks
- Delete tasks
- Task status tracking
- Priority management
- Due dates
- REST API for tasks
- Responsive web design

## Task Status

Tasks can be tracked as:

Pending → In Progress → Completed

## Priority Levels

- Low
- Medium
- High

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- Bootstrap
- MySQL Connector for Python

## API

GET /api/tasks

The API returns tasks belonging to the currently logged-in user.

## Database Tables

- users
- tasks

## How to Run

1. Install Python and MySQL.
2. Install dependencies:

   pip install -r requirements.txt

3. Import database.sql into MySQL.
4. Copy config.example.py and rename the copy to config.py.
5. Add your MySQL password to config.py.
6. Run:

   python app.py

7. Open:

   http://127.0.0.1:5000/register

## CRUD Operations

TaskFlow supports:

- Create - Add new tasks
- Read - View tasks
- Update - Edit task details and status
- Delete - Remove tasks

## Project Purpose

This project demonstrates full-stack web application development, authentication, CRUD operations, API integration, dynamic data handling, responsive design, and MySQL database integration.
