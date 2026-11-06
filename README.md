# CodeAlpha_EcommerceStore

A Django full-stack e-commerce internship project with product catalogue, product details, session-based cart, user authentication, checkout, order history, stock management, and Django admin.

## Requirements
- Python 3.10+
- VS Code
- Internet connection for Google Fonts and sample product photos (optional)

## Setup (Windows PowerShell)

1. Open this folder in VS Code.
2. Open Terminal > New Terminal.
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again.

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Create database tables:

   ```powershell
   python manage.py migrate
   ```

6. Add demonstration products:

   ```powershell
   python manage.py seed_products
   ```

7. (Optional) Create an admin account:

   ```powershell
   python manage.py createsuperuser
   ```

8. Start the server:

   ```powershell
   python manage.py runserver
   ```

9. Open http://127.0.0.1:8000/

## Admin
Open http://127.0.0.1:8000/admin/ and sign in with your superuser credentials. You can add, edit, deactivate, and update product stock. Orders appear here and can be updated through their status field.

## Main features
- Product catalogue and product detail pages
- Add/remove items in a session cart
- Account registration, login and logout
- Checkout form with cash-on-delivery demo flow
- Stock validation and deduction after order placement
- Customer order history
- Admin management for products and orders

## Important notes
- This is an internship/demo project. Checkout does not process real payments.
- The project uses SQLite for local development.
- Before public production deployment, configure a secure environment-based `SECRET_KEY`, set `DEBUG=False`, configure `ALLOWED_HOSTS`, HTTPS, email verification, payment integration, and production database/storage.
- Product photos are loaded from external Unsplash URLs and require internet access.
