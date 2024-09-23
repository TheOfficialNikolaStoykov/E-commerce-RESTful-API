# E-commerce RESTful API

This project provides a comprehensive E-commerce backend API built with Django REST framework. The API includes core functionalities for managing users, products, orders, carts, and shipping. It also supports user authentication, product reviews, and integrations with third-party services like Stripe and Shippo for payments and shipping.

## Features

- **User Management**: User registration, login, logout, profile management.
- **Product Management**: Add, update, delete, and view products and categories.
- **Order Management**: Place orders, view order history, manage order status.
- **Cart Management**: Add, edit, delete items from the cart.
- **Payment Integration**: Stripe integration for processing payments.
- **Shipping Integration**: Shippo integration for calculating shipping rates and managing deliveries.
- **Admin Access**: Admin-only features for managing products, categories, and order statuses.

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Django 4.x or higher
- Virtual environment setup (venv)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/TheOfficialNikolaStoykov/e-commerce-restful-api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd e-commerce-restful-api
    ```

3. Set up a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Run migrations to set up the database schema:

    ```bash
    python manage.py migrate
    ```

7. Create a superuser for accessing the Django admin:

    ```bash
    python manage.py createsuperuser
    ```

8. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

### API Documentation

API documentation is available via Swagger UI. You can access [here](https://theofficialnikolastoykov.github.io/e-commerce-restful-api/).

For example:

```
http://127.0.0.1:8000/swagger/
```

### Running Tests

To run tests, use the following command:

```bash
python manage.py test
```

To run coverage, use the following commands sequentially:
```bash
coverage run manage.py test
```
```bash
coverage report
```

## Technologies Used

- **Backend Framework**: Django REST Framework
- **Payment Integration**: Stripe API
- **Shipping Integration**: Shippo API
- **Authentication**: Django Token Authentication
- **Database**: SQLite
- **API Documentation**: Swagger UI

## License

This project is licensed under the MIT License - see the LICENSE file for details.
