# Django E-Commerce Platform

This is a feature-rich e-commerce platform built with Django. It includes Google login via `django-allauth`, a Stripe-powered checkout system, and an SQLite database.

---

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

4. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser (for accessing the Django admin):**

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to create your superuser account.

7. **Configure Google Login (`django-allauth`):**
    > **Note:** The login with Google feature will only work after you set up the Google OAuth credentials and update your Django project settings.
   - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create or select an existing project.
   - Go to **APIs & Services > Credentials** and create an OAuth 2.0 Client ID.
   - Set the redirect URI to:
     ```
     http://127.0.0.1:8000/accounts/google/login/callback/
     ```
   - Download the credentials file and update your Django project settings as needed.
   - For a step-by-step guide, refer to the following resources:
     - [Google Cloud Documentation](https://cloud.google.com/docs)
     - Video tutorials:
       - [Google OAuth Integration in Django - Tutorial 1](https://www.youtube.com/watch?v=yO6PP0vEOMc)
       - [Google OAuth with Allauth - Tutorial 2](https://www.youtube.com/watch?v=LyDdfO6o_G4)


8. **Configure Stripe Payment:**
    > **Note:** The checkout functionality will not work until you configure Stripe API keys in your project settings.
    - Log in to your [Stripe Dashboard](https://dashboard.stripe.com/).
    - Obtain your **Publishable Key** and **Secret Key**.
    - Update your `settings.py`:
        ```python
        from decouple import config

        STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
        STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
        ```

9. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000/`.

---

## Demo Images

<table>
  <tr>
    <td><img src="demo-image1.png" alt="Product Page" style="width: 100%;"/></td>
    <td><img src="demo-image2.png" alt="Checkout Page" style="width: 100%;"/></td>
  </tr>
  <tr>
    <td><img src="demo-image3.png" alt="Login Page" style="width: 100%;"/></td>
    <td><img src="demo-image4.png" alt="Admin Dashboard" style="width: 100%;"/></td>
  </tr>
  <tr>
    <td><img src="demo-image3.png" alt="Login Page" style="width: 100%;"/></td>
  </tr>
</table>

---
