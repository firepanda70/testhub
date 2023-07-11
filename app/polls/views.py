from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from app.settings import ELEMENTS_PER_PAGE

from .models import Poll, CompletedPool, Question


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
    completed = updated = False
    if user.is_authenticated:
        completed_poll = CompletedPool.objects.filter(user=user, origin=poll).order_by('-date_completed').first()
        if completed_poll:
            completed = True
            updated = poll.update_date > completed_poll.date_completed
    context = {
        'poll': poll,
        'completed': completed,
        'updated': updated,
        'question_amount': question_amount
    }
    return render(request, template, context)

@login_required
def take_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    template = 'polls/take_poll.html'
    questions = poll.questions.prefetch_related('options').all()
    if request.POST:
        raise NotImplementedError()
    context = {
        'questions': questions,
        'poll': poll
    }
    return render(request, template, context)
        