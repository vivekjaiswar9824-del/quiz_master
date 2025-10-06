from django.contrib import admin
from .models import Quiz, Question, Option, Submission, Answer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(Submission)
admin.site.register(Answer)
