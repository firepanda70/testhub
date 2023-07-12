import copy

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from app.settings import ELEMENTS_PER_PAGE

from .models import Poll, CompletedPool, AnsweredQuestion, ChosenOption
from .validators import validate_poll_form


def index(request):
    template = 'polls/index.html'
    polls = Poll.objects.all()
    paginator = Paginator(polls, ELEMENTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    rows = [[],]
    row = 0
    for obj in page.object_list:
        if len(rows[row]) == 3:
            rows.append([])
            row += 1
        rows[row].append(obj)

    context = {
        'page': page,
        'rows': rows
    }
    return render(request, template, context)

def poll_detail(request, poll_id):
    user = request.user
    template = 'polls/poll_detail.html'
    poll = get_object_or_404(Poll, pk=poll_id)
    question_amount = poll.questions.count()
    completed_id = updated = False
    if user.is_authenticated:
        completed_poll = CompletedPool.objects.filter(user=user, origin=poll).order_by('-date_completed').first()
        if completed_poll:
            completed_id = completed_poll.pk
            updated = poll.update_date > completed_poll.date_completed
    context = {
        'poll': poll,
        'completed_id': completed_id,
        'updated': updated,
        'question_amount': question_amount
    }
    return render(request, template, context)

@login_required
def take_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    template = 'polls/take_poll.html'
    questions = poll.questions.prefetch_related('options').all()
    questions_data = {
        str(question.pk): {
            'question': question,
            'options': {
                str(option.pk): option
                for option in question.options.all()
            }
        }
        for question in questions
    }
    errors = {}
    if request.POST:
        request_dict = dict(request.POST)
        token = request_dict.pop('csrfmiddlewaretoken')
        errors = validate_poll_form(questions, copy.deepcopy(request_dict))
        if not errors:
            try_count = CompletedPool.objects.filter(origin=poll, user=request.user).count() + 1
            completed_pool = CompletedPool.objects.create(
                user=request.user, origin=poll, attempt=try_count
            )
            answered_questions_by_id = {
                question_id: AnsweredQuestion.objects.create(
                origin=questions_data[question_id]['question'], pool=completed_pool
                ) for question_id in request_dict.pop('questions')
            }
            for option_id, option_data in request_dict.items():
                chosen = False
                if 'on' in option_data:
                    option_data.pop(option_data.index('on'))
                    chosen = True
                ChosenOption.objects.create(
                    origin=questions_data[option_data[0]]['options'][option_id],
                    is_chosen=chosen, question=answered_questions_by_id[option_data[0]]
                )
            for _, answered_question in answered_questions_by_id.items():
                answered_question.save()
            completed_pool.save()
            return redirect('polls:completed_poll_detail', completed_pool.pk)
    
    context = {
        'questions': {
            n: question for n, question in enumerate(questions, 1)
        },
        'poll': poll,
        'errors': errors
    }
    return render(request, template, context)

@login_required
def completed_polls(request):
    template = 'polls/completed_polls.html'
    polls = CompletedPool.objects.filter(user=request.user).all()
    paginator = Paginator(polls, ELEMENTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    rows = [[],]
    row = 0
    for obj in page.object_list:
        if len(rows[row]) == 3:
            rows.append([])
            row += 1
        rows[row].append(obj)

    context = {
        'page': page,
        'rows': rows
    }
    return render(request, template, context)

@login_required
def completed_poll_detail(request, poll_id):
    template = 'polls/completed_poll_detail.html'
    poll = get_object_or_404(CompletedPool, pk=poll_id)
    if poll.user != request.user:
        return redirect('polls:poll_detail', poll.origin.pk)
    answers = poll.questions.all()
    context = {
        'poll': poll,
        'answers': answers
    }
    return render(request, template, context)

def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )

def server_error(request):
    return render(request, 'misc/500.html', status=500)
