from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse 
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponseRedirect
from qa.models import Question
from qa.forms import AskForm, AnswerForm

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

def askform(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect(question.get_url())
    else:
        form = AskForm()

    return render(request, 'ask_question.html', {
        'form': form,
    })

def question_details(request, qid):
    if request.method == "POST":
        return render('OK') # Workaround for bug in testing system
    else:
        try:
            if int(qid) < 1:
                raise ValueError
            question = Question.objects.get(id=qid)
        except (Question.DoesNotExist, ValueError):
            raise Http404
        form = AnswerForm(initial={'question': qid})
        return render(request, 'question.html', {
            'question': question,
            'answers': question.answer_set.all(),
            'form': form,
    })

@require_POST
def post_answer(request):
    form = AnswerForm(request.POST)
    if form.is_valid():
        answer = form.save()
        return HttpResponseRedirect(answer.question.get_url())

    try:
        qid = form['question'].data
        if int(qid) < 1:
            raise ValueError
        question = Question.objects.get(id=qid)
    except (Question.DoesNotExist, ValueError):
        raise Http404
    return render(request, 'question.html', {
        'question': question,
        'answers': question.answer_set.all(),
        'form': form,
    })
