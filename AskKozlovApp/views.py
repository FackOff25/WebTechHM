from django.shortcuts import render
from django.core.paginator import Paginator
from . import fictionalDB
from .models import Question, Answer, Tag


# Create your views here.


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    iterators = paginator.get_page(page)
    return iterators


def new_questions(request):
    request.user = fictionalDB.USER
    iterators = paginate(Question.objects.get_new_questions(), request, 5)
    return render(request, 'newquestions.html', {'BestTags': Tag.objects.get_popular(6),
                                                 'BestUsers': fictionalDB.BESTUSERS, 'iterators': iterators})


def hot_questions(request):
    request.user = fictionalDB.USER
    iterators = paginate(Question.objects.get_hot_questions(), request, 5)
    return render(request, 'hotquestions.html', {'BestTags': Tag.objects.get_popular(6),
                                                 'BestUsers': fictionalDB.BESTUSERS, 'iterators': iterators})


# for now, it is just link to main page
def list_with_tags(request, tg):
    request.user = fictionalDB.USER
    iterators = paginate(Question.objects.get_questions_by_tag(tg), request, 5)
    return render(request, 'tag.html', {'BestTags': Tag.objects.get_popular(6),
                                        'BestUsers': fictionalDB.BESTUSERS, 'iterators': iterators, 'header': tg})


def signup(request):
    return render(request, "registration.html", {'BestTags': Tag.objects.get_popular(6),
                                                 'BestUsers': fictionalDB.BESTUSERS})


def login(request):
    return render(request, "login.html", {'BestTags': Tag.objects.get_popular(6),
                                          'BestUsers': fictionalDB.BESTUSERS})


# for now, it is just link to main page
def logout(request):
    return render(request, "include/index.html", {'BestTags': Tag.objects.get_popular(6),
                                                  'BestUsers': fictionalDB.BESTUSERS,
                                                  'questions': fictionalDB.QUESTIONS})


def settings(request):
    request.user = fictionalDB.USER
    return render(request, "settings.html", {'BestTags': Tag.objects.get_popular(6),
                                             'BestUsers': fictionalDB.BESTUSERS})


def ask(request):
    request.user = fictionalDB.USER
    return render(request, "newquestion.html", {'BestTags': Tag.objects.get_popular(6),
                                                'BestUsers': fictionalDB.BESTUSERS})


def question(request, qid: int):
    request.user = fictionalDB.USER
    the_question = Question.objects.get_question_by_id(qid)
    iterators = paginate(Answer.objects.get_by_question_id(qid), request, 5)
    return render(request, "question.html", {'BestTags': Tag.objects.get_popular(6),
                                             'BestUsers': fictionalDB.BESTUSERS,
                                             'isAsker': True,
                                             'question': the_question,
                                             'iterators': iterators})
