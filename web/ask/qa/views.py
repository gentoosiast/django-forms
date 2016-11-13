from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse 
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from django.core.urlresolvers import reverse
from qa.models import Question

def test(request, *args, **kwargs):
    return HttpResponse('OK')

@require_GET
def question_list(request, sort): 
    if sort == 'newest':
        qs = Question.objects.new()
    elif sort == 'popular':
        qs = Question.objects.popular()
    else:
        raise Http404

    try: 
        limit = int(request.GET.get('limit', 10)) 
    except ValueError: 
        limit = 10 
    if limit < 1 or limit > 100: 
        limit = 10 

    try: 
        page = int(request.GET.get('page', 1)) 
    except ValueError: 
        raise Http404 
    if page < 1:
        page = 1

    paginator = Paginator(qs, limit) 
    try: 
        page = paginator.page(page)
    except EmptyPage: 
        page = paginator.page(paginator.num_pages) 


    return render(request, 'qs_list.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })

@require_GET
def question_details(request, qid):
    try:
        question = Question.objects.get(id=qid)
    except Question.DoesNotExist:
        raise Http404
    return render(request, 'question.html', {
        'question': question,
        'answers': question.answer_set.all(),
    })
