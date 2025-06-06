# Daily Tasks App

This project is a simple web application designed to capture and track daily tasks using Streamlit for the frontend, FastAPI as the API layer, and SQLite for the database.

## Project Structure

```
daily-tasks-app
├── backend
│   ├── app.py          # Entry point for the FastAPI application
│   ├── database.py     # Handles SQLite database connection and session management
│   ├── models.py       # Defines database models using SQLAlchemy
│   ├── crud.py         # Contains CRUD operations for tasks
│   └── requirements.txt # Lists backend dependencies
├── frontend
│   ├── app.py          # Main Streamlit application for user interface
│   └── requirements.txt # Lists frontend dependencies
└── README.md           # Project documentation
```

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd daily-tasks-app
   ```

2. Set up the backend:
   - Navigate to the backend directory:
     ```
     cd backend
     ```
   - Install the backend dependencies:
     ```
     pip install -r requirements.txt
     ```

3. Set up the frontend:
   - Navigate to the frontend directory:
     ```
     cd ../frontend
     ```
   - Install the frontend dependencies:
     ```
     pip install -r requirements.txt
     ```

## Usage

1. Start the FastAPI backend:
   ```
   cd backend
   uvicorn app:app --reload
   ```

2. Start the Streamlit frontend:
   ```
   cd ../frontend
   streamlit run app.py
   ```

3. Open your web browser and go to `http://localhost:8501` to access the application.

## Features

- Capture daily tasks with a user-friendly interface.
- View, update, and delete tasks.
- Persistent storage using SQLite.

## License

This project is licensed under the ISC License.