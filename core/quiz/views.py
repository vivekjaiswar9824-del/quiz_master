from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, Question, Option
from .serializers import (
    QuizSerializer, QuizDetailSerializer, QuestionCreateSerializer,
    QuestionPublicSerializer, SubmissionSerializer
)
from .services import score_submission_and_create
from django.shortcuts import get_object_or_404

class QuizListCreateAPIView(APIView):
    """
    GET /api/quizzes/         -> list quizzes
    POST /api/quizzes/        -> create quiz { "title": "..." }
    """
    def get(self, request):
        qs = Quiz.objects.all().order_by("-created_at")
        data = QuizSerializer(qs, many=True).data
        return Response(data)

    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            quiz = serializer.save()
            return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizDetailAPIView(APIView):
    """
    GET /api/quizzes/{quiz_id}/ -> returns quiz with public questions (no correct info)
    """
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        serializer = QuizDetailSerializer(quiz)
        return Response(serializer.data)

class QuestionCreateAPIView(APIView):
    """
    POST /api/quizzes/{quiz_id}/questions/ -> add question with options
    payload example:
    {
      "text": "...",
      "question_type": "single",
      "expected_answer": "optional for text type",
      "options": [
         {"text": "A", "is_correct": false},
         {"text": "B", "is_correct": true}
      ]
    }
    """
    def post(self, request, quiz_id):
        data = request.data.copy()
        data["quiz"] = quiz_id
        serializer = QuestionCreateSerializer(data=data)
        if serializer.is_valid():
            q = serializer.save()
            return Response({"id": q.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizQuestionsAPIView(APIView):
    """
    GET /api/quizzes/{quiz_id}/questions_for_take/ -> returns questions with options (no correct flags)
    """
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        serializer = QuestionPublicSerializer(quiz.questions.all(), many=True)
        return Response(serializer.data)

class SubmitQuizAPIView(APIView):
    """
    POST /api/quizzes/{quiz_id}/submit/ -> submit answers and get score
    payload:
    {
      "answers": [
        { "question_id": 1, "selected_option_ids": [2] },
        { "question_id": 3, "text_answer": "..." }
      ]
    }
    """
    def post(self, request, quiz_id):
        data = request.data.copy()
        data["quiz_id"] = quiz_id
        serializer = SubmissionSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        payload = serializer.validated_data
        # scoring service returns score and total
        result = score_submission_and_create(payload["quiz_id"], payload["answers"])
        return Response({"score": result["score"], "total": result["total"]}, status=status.HTTP_200_OK)
