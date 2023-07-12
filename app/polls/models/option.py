from typing import Iterable, Optional
from django.db import models

from .base import BaseOption
from .question import Question, AnsweredQuestion


class Option(BaseOption):
    
    class Meta(BaseOption.Meta):
        pass

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Вопрос',
        help_text='Вариант ответа на вопрос'
    )
    
    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        return self.question.pool.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        return self.question.pool.save()


class ChosenOption(BaseOption):

    class Meta(BaseOption.Meta):
        pass

    origin = models.ForeignKey(
        Option,
        on_delete=models.SET_NULL,
        null=True
    )
    is_chosen = models.BooleanField(
        'Выбранный вариант',
        help_text='Выбранный вариант'
    )
    question = models.ForeignKey(
        AnsweredQuestion,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Вопрос',
        help_text='Вариант ответа на вопрос'
    )
    
    def save(self, *args, **kwargs) -> None:
        self.is_correct = self.origin.is_correct
        self.text = self.origin.text
        return super().save(*args, **kwargs)
