from django.shortcuts import render
from django.core.paginator import Paginator
from . import fictionalDB


# Create your views here.


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    iterators = paginator.get_page(page)
    return iterators


def new_questions(request):
    request.user = fictionalDB.USER
    iterators = paginate(fictionalDB.QUESTIONS, request, 5)
    return render(request, 'newquestions.html', {'title': "New", 'BestTags': fictionalDB.TAGS,
                                                 'BestUsers': fictionalDB.BESTUSERS, 'iterators': iterators})


def hot_questions(request):
    request.user = fictionalDB.USER
    iterators = paginate(fictionalDB.QUESTIONS, request, 5)
    return render(request, 'hotquestions.html', {'title': "Hot", 'BestTags': fictionalDB.TAGS,
                                                 'BestUsers': fictionalDB.BESTUSERS, 'iterators': iterators})


# for now, it is just link to main page
def list_with_tags(request, tg):
    request.user = fictionalDB.USER
    iterators = paginate(fictionalDB.QUESTIONS, request, 5)
    return render(request, 'tag.html', {'title': tg, 'BestTags': fictionalDB.TAGS,
                                        'BestUsers': fictionalDB.BESTUSERS, 'iterators': iterators, 'header': tg})


def signup(request):
    return render(request, "registration.html", {'title': "Sign Up", 'BestTags': fictionalDB.TAGS,
                                                 'BestUsers': fictionalDB.BESTUSERS})


def login(request):
    return render(request, "login.html", {'title': "Log In", 'BestTags': fictionalDB.TAGS,
                                          'BestUsers': fictionalDB.BESTUSERS})


# for now, it is just link to main page
def logout(request):
    return render(request, "include/index.html", {'title': "Main Page", 'BestTags': fictionalDB.TAGS,
                                                  'BestUsers': fictionalDB.BESTUSERS,
                                                  'questions': fictionalDB.QUESTIONS})


def settings(request):
    request.user = fictionalDB.USER
    return render(request, "settings.html", {'title': "Settings", 'BestTags': fictionalDB.TAGS,
                                             'BestUsers': fictionalDB.BESTUSERS})


def ask(request):
    request.user = fictionalDB.USER
    return render(request, "newquestion.html", {'title': "New Question", 'BestTags': fictionalDB.TAGS,
                                                'BestUsers': fictionalDB.BESTUSERS})


def question(request, qid: int):
    request.user = fictionalDB.USER
    iterators = paginate(fictionalDB.ANSWERS, request, 5)
    return render(request, "question.html", {'title': fictionalDB.QUESTIONS[qid]['title'],
                                             'BestTags': fictionalDB.TAGS,
                                             'BestUsers': fictionalDB.BESTUSERS,
                                             'isAsker': True,
                                             'question': fictionalDB.QUESTIONS[qid],
                                             'iterators': iterators})
