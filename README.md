Code Review Assistant:

A Django-based web application that allows users to upload source code files and receive AI-powered code reviews using Google Gemini.
The system analyzes the uploaded code and provides structured feedback on readability, bugs, performance, security, and overall improvements.

🚀 Features:

1. Code Upload Interface

Users can upload files written in Python, C, C++, Java (or any language).
The app reads the file, stores it, and sends its content to the LLM.

2. AI-Powered Code Review (Gemini)

The system generates a properly formatted review containing:

Summary

Line-by-line issues
Suggested improvements
Optional improved/refactored code snippet

3. Fallback Checklist

If the API key is missing or the LLM fails, the system returns a helpful manual checklist instead of crashing.

4. Clean Bootstrap UI

Upload page and report view are fully styled using Bootstrap for better UX.

5. Secure Key Handling

Uses .env for secrets
GEMINI_API_KEY=your_key_here

🏗️ Tech Stack:

Backend: Django (Python)
Frontend: Bootstrap 5, Django Templates
LLM: Google Gemini (via google-genai SDK)
Database: SQLite 
Storage: Local media folder for uploaded code

📁 Project Structure:

code_review_assistant/
│
├── code_review_assistant/     # Django project settings
├── reviews/                   # App logic
│   ├── templates/reviews/     # HTML templates
│   ├── models.py              # ReviewReport model
│   ├── views.py               # LLM integration + handlers
│   └── forms.py               # Upload form
│
├── media/                     # Uploaded code files
├── static/                    # CSS, JS
├── .env                       # Gemini API key (not committed)
├── db.sqlite3                 # Database
└── manage.py


⚙️ Installation:

step 1-
git clone <repo-url>
cd code_review_assistant
pip install -r requirements.txt

step 2-
GEMINI_API_KEY=your_key_here

step 3-
python manage.py runserver

📄 Example Use Cases:

Students uploading assignments
Developers reviewing code quickly
Teachers analyzing student submissions
Teams doing quick lint-style reviews

<img width="1919" height="1058" alt="image" src="https://github.com/user-attachments/assets/7e0e9f30-6abc-4ea8-a4fa-00be9907c971" />

<img width="1919" height="1059" alt="image" src="https://github.com/user-attachments/assets/710bfa35-91f0-4898-83a9-0eedaefbc65b" />
<img width="1919" height="1002" alt="image" src="https://github.com/user-attachments/assets/34795ed0-5eb7-4357-9876-d496e433231a" />

<img width="1445" height="495" alt="image" src="https://github.com/user-attachments/assets/4b9aa246-bcd8-44e2-b8be-cf500d357118" />

<img width="1919" height="753" alt="image" src="https://github.com/user-attachments/assets/8be3b4a4-1ac2-4f78-acc4-ddb0170a86a5" />

Snippet Video -
https://youtu.be/8g_acHFnWsU






