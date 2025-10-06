#  Online Quiz Application API

A simple **Django REST API** for creating, managing, and taking quizzes.  
Users can fetch quiz questions (without correct answers), submit answers, and get scores.

---

#  Features

#  Core Functionality
- **Quiz Management**
  - Create a quiz with a title.
  - Add questions to a quiz (single choice, multiple choice, or text type).
  - Options for each question with one or more correct answers.
- **Quiz Taking**
  - Fetch quiz questions for users (correct answers hidden).
  - Submit answers and get score in the format:
    ```json
    { "score": 3, "total": 5 }
    ```

# Bonus Features
- Validation:
  - Single choice: exactly one correct option.
  - Multiple choice: one or more correct options.
  - Text type: max 300 characters for the answer.
- Retrieve a list of all available quizzes.
- Optional unit tests for scoring and submission logic.

---

# Tech Stack & Versions

- **Backend:** Django 5.2+  
- **API Framework:** Django REST Framework 3.20+  
- **Database:** SQLite (default)  
- **Language:** Python 3.10+  
- **Testing:** Python `requests` library  
- **OS:** Cross-platform (Windows / macOS / Linux)  

---

#  Installation & Setup

# 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/online-quiz-api.git
cd online-quiz-api

#2️⃣ Create & activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

#3️⃣ Install dependencies
pip install -r requirements.txt

#4️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5️⃣ Run the Django server
python manage.py runserver


API will be accessible at:

http://127.0.0.1:8000/

# API Endpoints
Method         	Endpoint	                                     Description
POST	         /api/quizzes/                         	        Create a new quiz
GET	          /api/quizzes/                                 	List all quizzes
POST	        /api/quizzes/<quiz_id>/questions/       	      Add a question to a quiz
GET	          /api/quizzes/<quiz_id>/questions_for_take/    	Get questions (correct answers hidden)
POST	        /api/quizzes/<quiz_id>/submit/	                Submit answers & get score

Python Testing Script (All-in-One)

Create a file test_api.py and paste the following:

import requests

headers = {"Content-Type": "application/json"}

# Step 1: Create Quiz
quiz = requests.post(
    "http://127.0.0.1:8000/api/quizzes/",
    json={"title":"Sample Quiz"},
    headers=headers
)
print("Create Quiz Response:", quiz.json())

# Step 2: Add First Question
question1 = requests.post(
    "http://127.0.0.1:8000/api/quizzes/1/questions/",
    json={
        "text":"What is 2+2?",
        "question_type":"single",
        "options":[{"text":"3","is_correct":False},{"text":"4","is_correct":True}]
    },
    headers=headers
)
print("First Question Response:", question1.json())

# Step 3: Add Second Question
question2 = requests.post(
    "http://127.0.0.1:8000/api/quizzes/1/questions/",
    json={
        "text":"Which planet is known as the Red Planet?",
        "question_type":"single",
        "options":[
            {"text":"Earth","is_correct":False},
            {"text":"Mars","is_correct":True},
            {"text":"Jupiter","is_correct":False}
        ]
    },
    headers=headers
)
print("Second Question Response:", question2.json())

# Step 4: Fetch Questions for Taking
questions = requests.get("http://127.0.0.1:8000/api/quizzes/1/questions_for_take/")
print("Questions for Taking:", questions.json())

# Step 5: Submit Answers
submit = requests.post(
    "http://127.0.0.1:8000/api/quizzes/1/submit/",
    json={
        "answers":[
            {"question_id":1,"selected_option_ids":[2]},
            {"question_id":2,"selected_option_ids":[4]}
        ]
    },
    headers=headers
)
print("Submit Answers Response:", submit.json())


#Run the script:

python test_api.py

# Requirements (requirements.txt)
Django>=5.2
djangorestframework>=3.20
requests>=2.30

# Project Structure
quiz_api/
│
├── quiz/                   # Quiz app
│   ├── models.py           # Quiz, Question, Option models
│   ├── views.py            # API views
│   ├── serializers.py      # DRF serializers
│   ├── urls.py             # API routes
│
├── quiz_api/               # Django project folder
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
├── requirements.txt
├── test_api.py
└── README.md

