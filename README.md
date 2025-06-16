# BRU CSE 12 Website (Old Version)

> **Note**: This is the archived **old version** of the BRUR CSE 12 site. A newer, redesigned version is available separately.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Usage Guide](#usage-guide)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
  - [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Real-time Chat](#real-time-chat)
- [Testing](#testing)
- [Deployment](#deployment)
- [License](#license)
- [Contact](#contact)

## Overview

BRU CSE 12 is a community and learning platform for the Computer Science & Engineering department. It offers announcements, tutorials, online judge integrations, real-time chat, and COVID-19 data APIs.

## Features

- Announcement system (create, edit, delete)
- Tutorial browsing and management
- Real-time chat powered by Django Channels
- COVID-19 statistics API (global, country, district)
- Integration with Codeforces & URI online judges
- User registration, profile editing, password reset
- Problem listings and submission interface

## Usage Guide

1. **Browse Home**: View latest announcements and featured tutorials on the homepage (`/`).
2. **Announcements**: Go to `/ann/` to read announcements; authenticated users can add or edit.
3. **Tutorials**: Visit `/tutorial/` to explore topics, open individual tutorials, or submit new ones (login required).
4. **Chat**: Navigate to `/chat/` after logging in to exchange real-time messages with peers.
5. **Problems**: Check `/contests/` for problem listings; submit solutions via integrated online judge.
6. **Judge Info**: View external judge standings at `/jInfo/` and trigger manual updates.
7. **API**: Access COVID-19 data at `/api/` endpoints such as `/api/world/`, `/api/cnt=CountryName/`, `/api/dis=DistrictName/`.
8. **User Profile**: Manage your account under `/user/` for registration, profile edits, and password resets.

## Tech Stack

- Python 3.8+
- Django 3.x
- Django Channels (WebSockets)
- SQLite (default) or PostgreSQL
- Bootstrap 4, HTML5, CSS3, JavaScript

## Project Structure

```text
brurcse12/
├── api/           # COVID-19 API views & models
├── chat/          # Channels-based chat application
├── home/          # Landing pages, announcements, FAQs
├── judge_info/    # External judge data fetchers
├── problems/      # Problem listings & submissions
├── tutorial/      # Tutorial content management
├── user/          # Authentication and profile management
├── mysite/        # Django project settings & URLs
├── manage.py      # Django command-line utility
├── requirements.txt
├── Procfile       # Heroku deployment configuration
└── runtime.txt    # Python runtime version for Heroku
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip
- Git
- (Optional) Redis server for Django Channels in production

### Installation

```powershell
# Clone repository
git clone <repository-url> brurcse12
cd brurcse12

# Create and activate virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Database Setup

```powershell
# Apply migrations
python manage.py migrate

# (Optional) Create an admin user
python manage.py createsuperuser
```

### Running the Server

```powershell
# Start development server
python manage.py runserver
```

Open your browser to `http://127.0.0.1:8000/`.

## API Endpoints

- `GET /api/world/` – Global COVID-19 stats (JSON)
- `GET /api/cnt=<country>/` – Country-level stats
- `GET /api/dis=<district>/` – District-level stats
- `GET /api/dhaka=<area>/` – Detailed area stats
- `GET /api/force_update/` – Manually trigger data refresh

## Real-time Chat

- WebSocket URL: `ws://<host>/ws/chat/<room_name>/`
- Handled by `ChatConsumer` in `chat/consumers.py`.

## Testing

Run all unit tests:

```powershell
python manage.py test
```

## Deployment

- A `Procfile` is included for Heroku deployment:
  ```Procfile
  web: gunicorn mysite.wsgi --log-file -
  ```
- Configure environment variables such as `SECRET_KEY`, `DEBUG`, and `DATABASE_URL`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions, issues, or contributions, please contact the project maintainers or open an issue on the repository.
