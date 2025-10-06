from rest_framework import serializers
from .models import Quiz, Question, Option, Submission, Answer

class OptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text", "is_correct"]

class OptionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text"]  # no is_correct

class QuestionCreateSerializer(serializers.ModelSerializer):
    options = OptionCreateSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ["id", "quiz", "text", "question_type", "expected_answer", "options"]

    def validate(self, data):
        qtype = data.get("question_type", Question.QUESTION_TYPE_SINGLE)
        options = data.get("options", [])
        if qtype in (Question.QUESTION_TYPE_SINGLE, Question.QUESTION_TYPE_MULTIPLE):
            if not options or len(options) < 2:
                raise serializers.ValidationError("Choice questions must have at least 2 options.")
            # ensure at least one correct option
            if not any(o.get("is_correct", False) for o in options):
                raise serializers.ValidationError("At least one option must be marked correct.")
            if qtype == Question.QUESTION_TYPE_SINGLE:
                correct_count = sum(1 for o in options if o.get("is_correct", False))
                if correct_count != 1:
                    raise serializers.ValidationError("Single choice questions must have exactly one correct option.")
        else:  # text question
            # expected_answer optional but if present should be <= 300 words
            expected = data.get("expected_answer") or ""
            if expected and len(expected.split()) > 300:
                raise serializers.ValidationError("expected_answer exceeds 300 word limit")
        return data

    def create(self, validated_data):
        options_data = validated_data.pop("options", [])
        question = Question.objects.create(**validated_data)
        for opt in options_data:
            Option.objects.create(question=question, **opt)
        return question

class QuestionPublicSerializer(serializers.ModelSerializer):
    options = OptionPublicSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "text", "question_type", "options"]

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "title", "created_at"]

class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionPublicSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "questions"]

# Serializers for submission
class AnswerSubmissionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    text_answer = serializers.CharField(required=False, allow_blank=True)

class SubmissionSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = AnswerSubmissionSerializer(many=True)
