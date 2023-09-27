# Loan-Folio

A web-based loan management system built with Django, Django REST framework, and Celery.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Database Models](#database-models)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

Loan-Folio is a comprehensive loan management system designed to streamline the lending process. It handles user registrations, loan applications, credit scoring, loan disbursements, EMI calculations, and loan payments efficiently.

## Features

Loan-Folio offers the following features:

- **User Registration:** Users can create accounts with personal information.

- **Loan Application:** Users can apply for loans by providing necessary details.

- **Credit Scoring:** Credit scores are calculated asynchronously using Celery, helping in faster loan processing.

- **Statement Generation:** The system can generate statements detailing loan transactions and upcoming payments.

- **Loan Payment:** Users can make payments towards their loans, updating their remaining balance and loan status.

- **Loan Management:** View all loans and their details.

## Database Models

This project uses the following database models:

- **User:** Stores user information such as name, email, and annual income.

- **Loan:** Represents loan applications, including loan amount, interest rate, and disbursement date.

- **Transaction:** Records loan payments and details of each transaction.

## Requirements

Before you begin, ensure you have the following requirements installed:

- Python 3.6+
- Django 3.x
- Django REST framework
- Celery
- Redis (used as a message broker for Celery)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/LoanFolio.git
   cd LoanFolio
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv  #On Windows, virtualenv virtual_environment_name
   source venv/bin/activate  # On Windows, use: virtual_environment_name\Scripts\activate
   ```
3. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
    ```
4. Run database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Make a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```
6. Start redis-server and the Celery worker:
   ```bash
   redis-server
   celery -A LoanFolio worker --loglevel=info
   ```
7. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

## Usage

To use Loan-Folio, follow these steps:

1. **Access the Django Admin Panel:**

   Use the Django admin panel to manage users, loans, and transactions. Access it at [http://localhost:8000/admin/](http://localhost:8000/admin/).

2. **API Endpoints:**

   Use the following API endpoints to interact with the system:

   - **User Registration:** Register a new user.
     ```
     http://localhost:8000/api/register_user/
     ```

   - **Apply for a Loan:** Submit a loan application.
     ```
     http://localhost:8000/api/apply_loan/
     ```

   - **Make a Loan Payment:** Process a loan payment.
     ```
     http://localhost:8000/api/make_payment/
     ```

   - **Get a Loan Statement:** Retrieve a loan statement by specifying the loan ID (replace 'x' with the actual loan ID).
     ```
     http://localhost:8000/api/get-statement/?loan_id=x
     ```

   - **View All Loans:** Get a list of all loans and their details.
     ```
     http://localhost:8000/all-loans/
     ```
**If you have any questions or need further assistance, feel free to contact me:**

- Your Name: Gourav Yadav
- Email: gyadav88897@gmail.com

   



