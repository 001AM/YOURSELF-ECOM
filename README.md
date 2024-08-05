# E-commerce Django Project with Razorpay

## Introduction
This project is a simple e-commerce application built using Django, with Razorpay integrated for payment processing.

## Features
- Product listing and details
- Shopping cart
- Order management
- Payment via Razorpay

## Tech Stack
- **Backend:** Django
- **Database:** SQLite (default)
- **Payment Gateway:** Razorpay

## Installation

### Prerequisites
- Python 3.8+
- Razorpay account and API keys

### Setup Instructions
1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ecom-django-project.git](https://github.com/001AM/YOURSELF-ECOM.git
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables:**
    Create a `.env` file in the root directory and add the following:
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    RAZORPAY_KEY_ID=your_razorpay_key_id
    RAZORPAY_KEY_SECRET=your_razorpay_key_secret
    ```

5. **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage
1. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000`.

2. **Admin dashboard:**
   Go to `http://127.0.0.1:8000/admin` and log in with the superuser credentials to manage products and orders.

3. **Payment process:**
   Add products to your cart, proceed to checkout, and complete the payment using Razorpay.
