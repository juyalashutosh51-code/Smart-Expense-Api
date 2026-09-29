# Smart Expense API

A RESTful expense management and analytics API built with Python, FastAPI, SQLAlchemy, and Microsoft SQL Server.

## Overview

Smart Expense API is a backend application designed to manage financial transactions and provide useful spending insights through REST APIs.

The project uses a modular structure with separate routers, models, schemas, and service layers.

## Features

- Transaction management
- Income and expense tracking
- Category-based filtering
- Date-range filtering
- CSV transaction import
- Automatic transaction categorization
- Monthly financial summaries
- Category-level spending analysis
- Budget tracking
- Budget utilization and overspending analysis
- Transaction anomaly detection using Z-scores
- REST API documentation with Swagger/OpenAPI

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** Microsoft SQL Server
- **Data Processing:** Pandas
- **Validation:** Pydantic
- **API Testing:** Postman
- **Documentation:** Swagger/OpenAPI
- **Version Control:** Git & GitHub

## Project Structure

```text
Smart-Expense-Api/
│
├── app/
│   ├── models/
│   │   ├── budget.py
│   │   └── transaction.py
│   │
│   ├── routers/
│   │   ├── analytics.py
│   │   ├── budget.py
│   │   └── transaction.py
│   │
│   ├── schemas/
│   │   ├── budget.py
│   │   └── transaction.py
│   │
│   ├── services/
│   │   ├── anomaly_detector.py
│   │   └── categorizer.py
│   │
│   ├── database.py
│   └── main.py
│
├── .gitignore
└── requirements.txt

RUNNING THE PROJECT

1. Clone the repository

git clone https://github.com/juyalashutosh51-code/Smart-Expense-Api.git

cd Smart-Expense-Api


2. Create a virtual environment

python -m venv venv


3. Activate the virtual environment on Windows

venv\Scripts\activate


4. Install dependencies

pip install -r requirements.txt


5. Configure the database

Configure the application with your local Microsoft SQL Server database credentials using environment variables.

Do not commit .env files or database credentials to GitHub.


6. Start the API

uvicorn app.main:app --reload


The API will be available at:

http://127.0.0.1:8000


API DOCUMENTATION

FastAPI provides interactive API documentation through Swagger/OpenAPI.

After starting the application, the documentation can be accessed at:

http://127.0.0.1:8000/docs


AUTHOR

Ashutosh Juyal

LinkedIn:
https://www.linkedin.com/in/ashutosh-juyal-195620354/

GitHub:
https://github.com/juyalashutosh51-code