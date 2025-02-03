Mushroom E-Commerce Website
This is a full-featured Mushroom E-commerce website built using Python Django. The platform allows users to browse, purchase, and manage mushroom-related products efficiently.

Features

User Authentication: Signup, Login, Logout, and Profile Management

Product Catalog: List of available mushrooms with descriptions, images, and pricing

Shopping Cart: Add, update, or remove products from the cart

Order Management: Secure checkout, order tracking, and order history

Admin Panel: Manage users, products, orders, and more

Search & Filter: Find mushrooms easily using search and filter options

Payment Gateway: Integration with payment services for secure transactions

Tech Stack

Frontend: HTML, CSS, JavaScript, Bootstrap

Backend: Django, Django Rest Framework

Database: PostgreSQL / SQLite

Payment Gateway: Razorpay / Stripe

Deployment: AWS / Heroku

Installation Guide

Clone the repository:

git clone https://github.com/yourusername/mushroom-ecommerce.git
cd mushroom-ecommerce

Create and activate a virtual environment:

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Create a superuser for admin access:

python manage.py createsuperuser

Run the development server:

python manage.py runserver

Open the browser and visit:

http://127.0.0.1:8000/

Project Structure

📂 mushroom-ecommerce/
├── 📂 ecommerce/             # Main Django project folder
│   ├── settings.py           # Django settings
│   ├── urls.py               # URL configurations
│   ├── wsgi.py               # WSGI entry point
│   ├── asgi.py               # ASGI entry point
│   ├── __init__.py           # Package initialization
│
├── 📂 store/                 # Main app (Handles products, orders, cart, etc.)
│   ├── models.py             # Database models
│   ├── views.py              # Business logic
│   ├── urls.py               # App URL routing
│   ├── templates/            # HTML templates
│   ├── static/               # Static files (CSS, JS, images)
│   ├── forms.py              # Django forms
│   ├── admin.py              # Django admin configurations
│   ├── __init__.py           # Package initialization
│
├── 📂 media/                 # Uploaded user files (images, etc.)
├── 📂 static/                # Static assets
├── 📂 templates/             # Global HTML templates
├── manage.py                 # Django management script
├── requirements.txt          # Dependencies
├── README.md                 # Project documentation

Contribution Guide

Fork the repository.

Create a new branch for your feature or bug fix.

Commit your changes with a meaningful message.

Push the branch and create a pull request.

License

This project is licensed under the MIT License. Feel free to use and modify it!
