from .models import Quiz, Question, Option, Submission, Answer
from django.db import transaction

def score_submission_and_create(quiz_id: int, answers_payload: list) -> dict:
    """
    answers_payload: list of {question_id, selected_option_ids (list), text_answer (str)}
    returns dict with score and total and creates Submission & Answer records.
    """

    quiz = Quiz.objects.get(pk=quiz_id)
    questions = {q.id: q for q in quiz.questions.all().prefetch_related("options")}

    total_questions = len(questions)
    score = 0

    with transaction.atomic():
        submission = Submission.objects.create(quiz=quiz, total=total_questions, score=0)
        for ans in answers_payload:
            qid = ans.get("question_id")
            question = questions.get(qid)
            if question is None:
                # ignore unknown question ids (could also raise error)
                continue

            answer_obj = Answer.objects.create(submission=submission, question=question)
            # handle question types
            if question.question_type in (Question.QUESTION_TYPE_SINGLE, Question.QUESTION_TYPE_MULTIPLE):
                selected_ids = ans.get("selected_option_ids", []) or []
                if selected_ids:
                    # attach option instances (only those belonging to this question)
                    opts = question.options.filter(id__in=selected_ids)
                    answer_obj.selected_options.set(opts)
                    # scoring:
                    correct_opts = set(question.options.filter(is_correct=True).values_list("id", flat=True))
                    selected_set = set(opt.id for opt in opts)
                    if question.question_type == Question.QUESTION_TYPE_SINGLE:
                        # correct only if single chosen and it's the correct one
                        if len(selected_set) == 1 and selected_set == correct_opts:
                            score += 1
                    else:
                        # For multiple choice, award 1 point if EXACT match between selected and correct sets
                        if selected_set == correct_opts:
                            score += 1
                # else no answer selected -> zero
            else:  # text question
                text_ans = (ans.get("text_answer") or "").strip()
                answer_obj.text_answer = text_ans
                # naive grading: if expected_answer provided, do case-insensitive exact match trimming whitespace
                if question.expected_answer:
                    if text_ans and text_ans.lower().strip() == question.expected_answer.lower().strip():
                        score += 1
                # else can't auto-grade (left as zero). You could implement fuzzy matching later.
                answer_obj.save()
        submission.score = score
        submission.save()

    return {"score": score, "total": total_questions, "submission_id": submission.id}
