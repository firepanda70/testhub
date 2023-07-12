def validate_poll_form(questions, form_data: dict):
    question_data = {
        str(question.pk): {
            'object': question,
            'options_ids': {
                str(option.pk): option
                    for option in question.options.all()
            },
            'ansvered': False
        }
        for question in questions
    }
    errors = {}
    if 'questions' not in form_data:
        errors['questions'] = 'Отсутствует поле'
    else:
        form_answers = form_data.pop('questions')
        if not form_answers or len(form_answers) != len(question_data):
            errors['questions-amount'] = 'Не на все вопросы был дан ответ'
        else:
            for el in form_answers:
                if el not in question_data:
                    errors[f'option-{el}'] = 'Неверный идентфикатор'
        for option_id, option_data in form_data.items():
            on = False
            if 'on' in option_data:
                option_data.pop(option_data.index('on'))
                on = True
            if len(option_data) == 0:
                errors[f'option-{option_id}'] = 'Отстутствует поле'
                continue
            origin = option_data[0]
            if origin not in question_data:
                errors[f'question-{origin}'] = 'Неверный идентфикатор'
                continue
            if option_id not in question_data[origin]['options_ids']:
                errors[f'question-{origin} option-{option_id}'] = 'Неверная пара индентификаторов'
                continue
            if not question_data[origin]['ansvered']:
                question_data[origin]['ansvered'] = on
    for id in question_data:
        if not question_data[id]['ansvered']:
           errors[f'question-{id}'] = 'Не был дан ответ на вопрос'
    return errors
