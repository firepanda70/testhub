from typing import Any, Dict, Iterable, Optional, Tuple
from django.db import models

from .base import BaseQuestion
from .pool import Poll, CompletedPool


class Question(BaseQuestion):
    
    class Meta(BaseQuestion.Meta):
        pass

    pool = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Тест',
        help_text='Вопрос теста'
    )
    is_active = models.BooleanField(
        'Включен в тест',
        help_text=('Включен в тест. В случае если активных вопросов в тесте '
                   'станет меньше 2, тест автоматически снимется с публикации.')
    )

    def check_active_questions(self):
        questions = Question.objects.filter(pool=self.pool.pk)
        if len([el for el in questions if el.is_active == True]) < 2:
            return self.pool.deactivate()
        return self.pool.save()

    def save(self, *args, **kwargs) -> None:
        res = super().save(*args, **kwargs)
        self.check_active_questions()
        return res

    def delete(self, *args, **kwargs) -> Tuple[int, dict[str, int]]:
        res = super().delete(*args, **kwargs)
        self.check_active_questions()
        return res


class AnsweredQuestion(BaseQuestion):

    class Meta(BaseQuestion.Meta):
        pass

    origin = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True
    )
    pool = models.ForeignKey(
        CompletedPool,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Тест',
        help_text='Вопрос теста'
    )
    is_correct = models.BooleanField(
        'Правильность ответа',
        help_text='Правильность ответа'
    )
