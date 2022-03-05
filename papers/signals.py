from django.db.models.signals import post_save
from django.dispatch import receiver

from papers.models import QuestionUser


@receiver(post_save, sender=QuestionUser)
def question_user_saved(sender, instance, created, *args, **kwargs):
    if created:
        question = instance.question
        question.solved_count += 1
        if (not instance.is_correct):
            question.wrong_count += 1
        question.wrong_answer_rate = round(question.wrong_count/question.solved_count, 3)
        question.save()
