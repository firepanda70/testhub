from django.db import models


class BaseOption(models.Model):

    class Meta:
        abstract = True
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    text = models.CharField(
        'Вариант ответа',
        max_length=50,
        help_text='Вариант ответа'
    )
    is_correct = models.BooleanField(
        'Верный ответ',
        help_text='Верный ли ответ'
    )

    def __str__(self):
        return self.text

class BaseQuestion(models.Model):

    class Meta:
        abstract = True
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    text = models.CharField(
        'Текст вопроса',
        max_length=200,
        help_text='Текст вопроса'
    )

    def __str__(self):
        return self.text


class BasePool(models.Model):

    class Meta:
        abstract = True
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    title = models.CharField(
        'Заголовок',
        max_length=100,
        help_text='Название теста'
    )

    def __str__(self):
        return self.title
