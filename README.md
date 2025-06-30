# 203-Investigative-Studio-I

As part of my second year studying Software Engineering at Yoobee Colleges, I developed this full-stack web application that integrates Flask, JavaScript/HTML, and a SQL database to create a modular, secure, and AI-enhanced platform.

**OVERVIEW**

This project demonstrates my ability to:

- Build scalable, secure backend services using Flask

- Develop responsive, user-friendly frontend interfaces with HTML, CSS, and JavaScript

- Implement data storage using SQL databases

- Integrate AI through the OpenAI API

- Design modular systems and manage multiple codebases efficiently

**KEY FEATURES**

-Secure User Authentication:
    Uses SHA-based encryption for handling user credentials securely.

-AI Integration:
     Dynamic, real time responses using the OpenAI API.

-Modular Architecture:
    Backend logic, data processing, and testing are separated into independent, well-organized scripts.

-SQL Database Support:
    Stores user data and session information with reliability and scalability.

-Email Automation:
    Includes functionality for sending automated emails for password recovery and email confirmation.

-Spam handling:
    User cooldowns for requests such as openAI requests and email sending have cooldowns managed through JavaScript and through Flask cookies.

**TECH STACK**

Backend: Python (Flask)

Frontend: HTML, CSS, JavaScript

Database: SQLite - PostgreSQL

AI Integration: OpenAI API

Security: SHA encryption

**HOW TO RUN**

1.    Clone the repository: git clone https://github.com/MitchellWillis05/-Fullstack-Flask-Web-App-203-Investigative-Studio-I
2.    Install dependencies: pip install -r requirements.txt
3.    Set up environment variables: OPENAI_API_KEY="your-api-key", MAIL_PASSWORD=:your-mail-password"
4.    Run the application: py main.py
