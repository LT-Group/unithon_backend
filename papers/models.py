from django.db import models

# Create your models here.
from unithon_backend import settings


class Paper(models.Model):
    test_audio_file = models.FileField(upload_to='test_audio_file/%Y/%m/%d', null=True, blank=True, help_text="테스트 음성파일")
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True)


class PaperUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='paper_user')
    paper = models.ForeignKey('papers.Paper', help_text='시험', on_delete=models.CASCADE, related_name='paper_user')
    total_score = models.IntegerField(help_text='총점', default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    paper = models.ForeignKey('papers.Paper', help_text='시험', on_delete=models.CASCADE, related_name='question')
    answer = models.CharField(help_text='정답', max_length=50)
    solved_count = models.IntegerField(help_text='푼 사람 수', default=0)
    wrong_count = models.IntegerField(help_text='틀린 사람 수', default=0)
    wrong_answer_rate = models.FloatField(help_text='오답률', default=0)


class QuestionUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='유저가 푼 시험 문제', on_delete=models.CASCADE,
                             related_name='question_user')
    question = models.ForeignKey('papers.Question', help_text='시험 문제', on_delete=models.CASCADE,
                                 related_name='question_user')
    answer_user = models.CharField(help_text='유저가 작성한 정답', max_length=50)
    is_correct = models.BooleanField(help_text='정답 여부')

