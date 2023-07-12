from typing import Iterable, Optional
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models

from .base import BasePool

User = get_user_model()


class Poll(BasePool):
    
    class Meta(BasePool.Meta):
        ordering = ('-create_date', )

    description = models.CharField(
        'Описание',
        help_text='Описание теста'
    )
    create_date = models.DateTimeField(
        'Дата создания',
        help_text='Дата создания',
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        'Дата обновления',
        help_text='Дата обновления',
        auto_now_add=True,
    )
    is_active = models.BooleanField(
        'Опубликован',
        help_text=(
            'Если выбрана, прохождение доступно для пользователей. '
            'Должно быть как минимум 2 вопроса'
        ),
        default=False
    )

    def clean(self):
        if self.is_active and self.pk and self.questions.filter(is_active=True).count() < 2:
            raise ValidationError({'is_active': 'Для публикации в тесте должно быть минимум 2 включеных вопроса'})
        
    def deactivate(self):
        if self.is_active:
            self.is_active = False
            return self.save(update_fields=['is_active'])

    def save(self, *args, **kwargs) -> None:
        self.update_date = timezone.now()
        return super().save(*args, **kwargs)


class CompletedPool(BasePool):

    class Meta(BasePool.Meta):
        verbose_name = 'Завершенный тест'
        verbose_name_plural = 'Завершенные тесты'
        ordering = ('-date_completed', )

    user = models.ForeignKey(
        User,
        verbose_name='Прошедший тест',
        help_text='Прошедший тест',
        on_delete=models.CASCADE
    )
    origin = models.ForeignKey(
        Poll,
        on_delete=models.SET_NULL,
        null=True
    )
    question_amount = models.IntegerField(
        'Общее количество вопросов',
        help_text='Общее количество вопросов',
        default=0
    )
    correct_answers_amount = models.IntegerField(
        'Количество правильных ответов',
        help_text='Количество правильных ответов',
        default=0
    )
    date_completed = models.DateTimeField(
        'Дата завершения',
        help_text='Дата завершения',
        auto_now_add=True,
    )
    attempt = models.IntegerField(
        'Номер попытки',
        help_text='Номер попытки'
    )

    @property
    def persentage(self):
        return int(self.correct_answers_amount / self.question_amount * 100)

    def save(self, *args, **kwargs) -> None:
        self.title = self.title or self.origin.title
        if self.pk:
            questions = self.questions
            self.question_amount = questions.count()
            self.correct_answers_amount = questions.filter(is_correct=True).count()
        return super().save(*args, **kwargs)
