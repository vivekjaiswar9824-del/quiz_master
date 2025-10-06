from django.urls import path
from .views import (
    QuizListCreateAPIView, QuizDetailAPIView,
    QuestionCreateAPIView, QuizQuestionsAPIView, SubmitQuizAPIView
)

urlpatterns = [
    path("quizzes/", QuizListCreateAPIView.as_view(), name="quiz-list-create"),
    path("quizzes/<int:quiz_id>/", QuizDetailAPIView.as_view(), name="quiz-detail"),
    path("quizzes/<int:quiz_id>/questions/", QuestionCreateAPIView.as_view(), name="question-create"),
    path("quizzes/<int:quiz_id>/questions_for_take/", QuizQuestionsAPIView.as_view(), name="questions-for-take"),
    path("quizzes/<int:quiz_id>/submit/", SubmitQuizAPIView.as_view(), name="quiz-submit"),
]
