FastAPI Login
A lightweight login and registration system built with FastAPI, SQLite, and Jinja2 templates. This project demonstrates how to set up user authentication in a FastAPI application.

Features
- User registration
- Login and logout functionality
- SQLite database for storing user credentials
- Jinja2 templates for rendering HTML pages
- Static file support (CSS, JS, images)


Installation
- Clone the repository:
git clone https://github.com/dibyendu68/fast_api_login.git
cd fast_api_login
- Create a virtual environment:
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
- Install dependencies:
pip install fastapi uvicorn jinja2
- Run the application:
uvicorn main:app --reload



Project Structure
fast_api_login/
│── main.py        # Application entry point
│── users.db       # SQLite database
│── templates/     # Jinja2 HTML templates
│── static/        # Static files (CSS, JS)


© 2026 Dibyendu68. All rights reserved.





