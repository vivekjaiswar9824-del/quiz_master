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

# create superuser
username : admin
password : 1234


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

###  Create a file test_api.py and paste the following:

import requests

# Step 1: Create a new quiz
url = "http://127.0.0.1:8000/api/quizzes/"
data = {"title": "Sample Quiz"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
print("📘 Create Quiz Response:")
print(response.json())
print("------------------------------------------------")

# Step 2: Add a question to the quiz (Quiz ID = 1)
question_url = "http://127.0.0.1:8000/api/quizzes/1/questions/"
question_data = {
    "text": "1. What does the Acronym REST Stand for?",
    "question_type": "single",
    "options": [
        {"text": "Representational State protocol", "is_correct": False},
        {"text": "Representational State Transfer", "is_correct": True}
    ]
}

question_response = requests.post(question_url, json=question_data, headers=headers)
print(" Add Question Response:")
print(question_response.json())
print("------------------------------------------------")

# Step 3: Fetch questions for taking (no correct answers)
take_url = "http://127.0.0.1:8000/api/quizzes/1/questions_for_take/"
take_response = requests.get(take_url)
print(" Questions For Taking:")
print(take_response.json())
print("------------------------------------------------")

# Step 4: Submit answers
submit_url = "http://127.0.0.1:8000/api/quizzes/1/submit/"
submit_data = {
    "answers": [
        {"question_id": 1, "selected_option_ids": [2]}  # Assuming option 2 is correct
    ]
}
submit_response = requests.post(submit_url, json=submit_data, headers=headers)
print(" Submit Answers Response:")
print(submit_response.json())
print("------------------------------------------------")


# Step 2b: Add another question to the same quiz (Quiz ID = 1)
question_data_2 = {
    "text": "give me the api full form",
    "question_type": "single",
    "options": [
        {"text": "application interface perogramming", "is_correct": False},
        {"text": "application programming interface", "is_correct": True},
        {"text": "app program input", "is_correct": False}
    ]
}

question_response_2 = requests.post(
    "http://127.0.0.1:8000/api/quizzes/1/questions/",
    json=question_data_2,
    headers=headers
)

print("🧩 Add Second Question Response:")
print(question_response_2.json())
print("------------------------------------------------")

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

