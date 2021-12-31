from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


def get_default_start_date():
    return now() + timedelta(hours=1)


def get_default_end_date():
    return now() + timedelta(days=1, hours=1)


class Quiz(models.Model):
    quiz_name = models.CharField(
        _('название опроса'),
        max_length=128
    )
    quiz_description = models.CharField(
        _('описание опроса'),
        max_length=4000,
    )
    start_date = models.DateTimeField(
        _('дата начала опроса'),
        default=get_default_start_date,
    )
    end_date = models.DateTimeField(
        _('дата окончания опроса'),
        default=get_default_end_date
    )

    # можно и так, если есть потребность не удалять сущности. Написал для примера, нигде не реализовывал
    # is_active = models.BooleanField(
    #     _('Активный')
    # )

    def __str__(self):
        return f'[{self.pk}] {self.quiz_name} ({self.start_date} - {self.end_date})'

    @staticmethod
    def get_base_filtered(is_superuser=None, pk=None):
        qs = Quiz.objects.all().order_by('-start_date')
        if not is_superuser:
            qs = qs.filter(end_date__gte=now())  # получение активных опросов. Можно еще по полю is_active проверять, но я
        if pk:
            qs = qs.filter(pk=pk)
        return qs


class Question(models.Model):
    TEXT = 1
    SINGLE = 2
    MULTI = 3
    # проверок на корректный ввод я не делал
    QUESTION_TYPE_CHOICES = [
        (TEXT, 'текстовый'),
        (SINGLE, 'выбор одного варианта'),
        (MULTI, 'выбор нескольких вариантов'),
    ]

    quiestion_text = models.CharField(
        _('текст вопроса'),
        max_length=512,
    )
    question_type = models.PositiveSmallIntegerField(
        _('тип вопроса'),
        choices=QUESTION_TYPE_CHOICES,
        default=SINGLE,
    )
    quiz = models.ForeignKey(
        Quiz,
        verbose_name=_('опрос'),
        on_delete=models.CASCADE,  # при использовании "is_active" можно тоже помечать неактивным, вместо удаления
    )

    def __str__(self):
        return f'[{self.quiz.pk}] [{self.pk}] {self.quiestion_text[:10]}...'


class PossibleAnswer(models.Model):
    answer_text = models.CharField(
        _('возможный вариант ответа'),
        max_length=512,
    )
    question = models.ForeignKey(
        Question,
        verbose_name=_('вопрос'),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'[{self.question.quiz.pk}] [{self.question.pk}] [{self.pk}] {self.answer_text[:10]}...'


class UserAnswer(models.Model):
    answered_by = models.ForeignKey(
        get_user_model(),
        verbose_name=_('кто ответил'),
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        _('текстовый ответ пользователя'),
        max_length=4000,
        blank=True,
    )
    possible_answer = models.ForeignKey(
        PossibleAnswer,
        verbose_name=_('вариант ответа'),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'[{self.possible_answer.question.quiz.pk}] [{self.possible_answer.question.pk}] [{self.possible_answer.pk}] [{self.pk}] {self.text[:10]}'
