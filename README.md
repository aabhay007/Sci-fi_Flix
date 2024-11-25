# ScifiFlix

ScifiFlix is a Django-based web application that allows users to explore and discover science fiction movies. The application supports user authentication via email or phone number, and utilizes One-Time Passwords (OTP) for secure login.

## Features

- User registration and login using email or phone number.
- OTP verification for secure authentication.
- Display of trending movies and new releases.
- Admin panel to manage movies and categories.

## Technologies Used

- Django 5.1.2
- SQLite (default database)
- Twilio for SMS notifications (optional)   pip install twilio sendgrid
- SMTP for email notifications (using Gmail)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aabhay007/scififlix.git
   cd scififlix
