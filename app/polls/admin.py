from django.core.exceptions import ValidationError
from django import forms
from django.forms.models import BaseInlineFormSet
from django.contrib import admin

from .models import (
    Poll, Question, Option,
    AnsweredQuestion, ChosenOption, CompletedPool
)


class PoolCreateForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = '__all__'
        widgets = {
            "is_active": forms.CheckboxInput(attrs={'disabled': 1}),
        }


class PoolUpdateForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = '__all__'


class OptionInlineFormSet(BaseInlineFormSet):
    def clean(self) -> None:
        super(OptionInlineFormSet, self).clean()
        answers_values = [
            form.cleaned_data['is_correct'] for form in self.forms if (
            form.cleaned_data and not form.cleaned_data.get('DELETE'))
        ]
        if len(answers_values) < 2:
            raise ValidationError('Должно быть минимум 2 варианта ответа')
        if all(value == answers_values[0] for value in answers_values):
            raise ValidationError('Должен быть минимум 1 не верный и 1 верный вариант ответа')


class OptionInline(admin.TabularInline):
    model = Option
    formset = OptionInlineFormSet


@admin.register(Question)
class AdminZoneQuestion(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pool',)
    inlines = (OptionInline,)


@admin.register(Poll)
class AdminZonePoll(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'create_date', 'update_date', 'description', 'is_active'
    )
    search_fields = ('title',)
    empty_value_display = '-пусто-'

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form = PoolUpdateForm
        else:
            self.form = PoolCreateForm
        return super(AdminZonePoll, self).get_form(request, obj, **kwargs)


@admin.register(CompletedPool)
class AdminZoneCompletedPool(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'origin', 'user', 'question_amount',
        'correct_answers_amount', 'persentage', 'attempt'
    )
    readonly_fields = (
        'origin', 'user', 'question_amount', 'title',
        'correct_answers_amount', 'persentage', 'attempt'
    )

@admin.register(AnsweredQuestion)
class AdminZoneAnsweredQuestion(admin.ModelAdmin):
    list_display = (
        'pk', 'text', 'pool', 'origin', 'is_correct'
    )
    readonly_fields = (
        'text', 'pool', 'origin', 'is_correct'
    )