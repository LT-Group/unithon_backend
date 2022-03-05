from django.contrib import admin

# Register your models here.
from papers.models import Paper, PaperUser, Question, QuestionUser


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['pk', 'test_audio_file']

@admin.register(PaperUser)
class PaperUserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'paper', 'total_score']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'paper', 'answer', 'solved_count', 'wrong_count', 'wrong_answer_rate']

@admin.register(QuestionUser)
class QuestionUserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'question', 'answer_user', 'is_correct']