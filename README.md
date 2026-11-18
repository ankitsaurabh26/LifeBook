### Environment Setup

#### Step 1: Create a virtual environment

> python3 -m venv myenv

#### Step 2: Activate the virtual environment

> source ./myenv/bin/activate

#### Step 3: Install dependencies

> pip install fastapi uvicorn pydantic

#### Step 4: Verify installed packages

> pip list

---

### MySQL Database Setup

#### Step 1: Change the MySQL root user's password (if needed)

Run in the SQL Workbench

> FLUSH PRIVILEGES;

> ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewStrongPassword';

#### Step 2: Install database dependencies

> pip install sqlalchemy pymysql

#### Initial Project Structure

Create the following three Python files:

- **database.py** – Connects Python to MySQL and provides database sessions
- **models.py** – Defines database tables and their columns using SQLAlchemy
- **schema.py** – Validates incoming data and structures outgoing API responses using Pydantic

**main.py** - contains the API endpoints that coordinate everything

---

### Overall Data Flow:

> Frontend (JSON) → FastAPI → Schema Validation → API Logic → SQLAlchemy → MySQL Database → Response Schema → JSON Response → Frontend

### How Data Flows in the Application

The application follows a structured flow to process data between the frontend, FastAPI backend, and MySQL database.

1. **Frontend:** The user performs an action, such as creating a new habit. The frontend sends the habit details to the backend as a JSON object through an API request.

2. **Schema Validation (`schemas.py`):** FastAPI uses Pydantic schemas, such as `HabitCreate`, to validate the incoming JSON data. It checks whether the required fields are present and whether their values have the correct data types. Invalid data is rejected before reaching the API logic.

3. **API Logic (`main.py`):** Once the data is validated, the API endpoint receives it and performs the required operation. For example, when creating a habit, it creates a new SQLAlchemy object using the validated data.

4. **Database Interaction (`models.py` and `database.py`):** SQLAlchemy maps the Python object to the corresponding MySQL table. The database session performs operations such as inserting, updating, retrieving, or deleting records.

5. **Response Schema (`HabitOut` in `schemas.py`):** After the database operation, the API returns the resulting SQLAlchemy object. `HabitOut` defines the structure of the response and converts the ORM object's attributes into a JSON-compatible format.

6. **Frontend Response:** FastAPI sends the final JSON response to the frontend, where the application displays the updated information to the user.

---
