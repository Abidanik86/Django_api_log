Django API + Logs Project
This project is designed to log API requests and responses automatically using a custom middleware. By integrating this app into your Django project, you can capture and store valuable information about your API interactions for monitoring, debugging, and auditing purposes.

Features
Logs all incoming API requests, including headers, body, and query parameters.
Logs all outgoing API responses, including status codes and response bodies.
Easily customizable to add or exclude specific paths or headers.
Installation and Setup
Clone the Repository
Clone this repository to your Django project directory.

Install the App
Add the app to your Django project's INSTALLED_APPS in settings.py:

python
Copy code
INSTALLED_APPS = [
    ...
    'your_app_name',  # Replace 'your_app_name' with the name of the app containing the API log functionality
]
Apply Database Migrations
Run the following commands to create the database table for storing API logs:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Add Middleware
Add the API log middleware to your MIDDLEWARE settings in settings.py:

python
Copy code
MIDDLEWARE = [
    ...
    'your_app_name.middleware.APILogMiddleware',  # Replace 'APILogMiddleware' with the middleware class
]
Include URL Paths
Ensure your project's urls.py file includes the necessary paths for the API endpoints.

Usage
Once the app is installed and configured, it will automatically log all API requests and responses. The logs can be reviewed by querying the database model created for storing API logs.

Contributing
Contributions are welcome! Please submit issues or pull requests to improve the project.
