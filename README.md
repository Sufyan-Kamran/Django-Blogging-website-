Medium Clone Project

A full-stack blog application inspired by Medium, built with Django for the backend and a separate frontend repository. This project allows users to create, read, update, and delete blog posts, comment on posts, and manage their accounts.

Features

User Authentication

Sign up, log in, and log out

JWT-based authentication for secure API access

Blog Posts

Create, read, update, and delete posts

Categorize posts with predefined categories

Comments

Add, edit, and delete comments

Only comment authors can modify their own comments

Search & Filtering

Search posts by title or content

Filter posts by category or author

Frontend & Backend Separation

Backend API built with Django REST Framework

Frontend built separately (React or any framework)

Environment Management

.env support for sensitive credentials

venv for Python dependencies (ignored by Git)

Tech Stack

Backend: Django, Django REST Framework, SQLite/PostgreSQL

Frontend: React (stored in medium_frontend repo)

Authentication: JWT (JSON Web Tokens)

Other Tools: Git, GitHub, Postman (for API testing)

Installation

Clone the repository

git clone <main-repo-url>
cd medium_clone


Set up virtual environment

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


Install backend dependencies

pip install -r requirements.txt


Run migrations

python manage.py makemigrations
python manage.py migrate


Run the server

python manage.py runserver


Frontend
Clone and set up the frontend separately:

git clone <frontend-repo-url> medium_frontend
cd medium_frontend
npm install
npm start

Usage

Visit http://localhost:8000 to access the backend API

Frontend will run on http://localhost:3000 (React default)

Use Postman or frontend UI to test API endpoints

Project Structure
medium_clone/
├─ backend/                  # Django project files
├─ medium_frontend/          # Separate frontend repo
├─ venv/                     # Python virtual environment (ignored)
├─ .gitignore
├─ README.md
└─ requirements.txt