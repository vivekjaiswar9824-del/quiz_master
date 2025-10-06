from django.db import models
from django.core.exceptions import ValidationError

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPE_SINGLE = "single"
    QUESTION_TYPE_MULTIPLE = "multiple"
    QUESTION_TYPE_TEXT = "text"

    QUESTION_TYPES = [
        (QUESTION_TYPE_SINGLE, "Single Choice"),
        (QUESTION_TYPE_MULTIPLE, "Multiple Choice"),
        (QUESTION_TYPE_TEXT, "Text"),
    ]

    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(
        max_length=10, choices=QUESTION_TYPES, default=QUESTION_TYPE_SINGLE
    )
    # for text questions you may want an expected answer for auto-grading:
    expected_answer = models.TextField(blank=True, null=True)

    def clean(self):
        # If text question, limit expected_answer length to 300 words if provided
        if self.question_type == self.QUESTION_TYPE_TEXT and self.expected_answer:
            if len(self.expected_answer.split()) > 300:
                raise ValidationError("expected_answer exceeds 300 word limit")

    def __str__(self):
        return f"{self.pk}: {self.text[:50]}"

class Option(models.Model):
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Option {self.pk} for Q{self.question_id}"

    class Meta:
        # ensure option text uniqueness per question is optional but helpful
        unique_together = ("question", "text")

class Submission(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="submissions", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # you could store user reference if you implement users
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

class Answer(models.Model):
    submission = models.ForeignKey(Submission, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # selected options for choice questions
    selected_options = models.ManyToManyField(Option, blank=True)
    # for text answers
    text_answer = models.TextField(blank=True, null=True)

    def clean(self):
        # Validation: text answer length if present
        if self.text_answer and len(self.text_answer.split()) > 300:
            raise ValidationError("text_answer exceeds 300 word limit")
