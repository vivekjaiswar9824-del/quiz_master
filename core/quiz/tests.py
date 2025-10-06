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
    "text": "What is 2 + 2?",
    "question_type": "single",
    "options": [
        {"text": "3", "is_correct": False},
        {"text": "4", "is_correct": True}
    ]
}

question_response = requests.post(question_url, json=question_data, headers=headers)
print("🧩 Add Question Response:")
print(question_response.json())
print("------------------------------------------------")

# Step 3: Fetch questions for taking (no correct answers)
take_url = "http://127.0.0.1:8000/api/quizzes/1/questions_for_take/"
take_response = requests.get(take_url)
print("📝 Questions For Taking:")
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
print("✅ Submit Answers Response:")
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
