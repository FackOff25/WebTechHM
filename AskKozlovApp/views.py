from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse

from django.contrib.auth.models import User
from AskKozlovApp.models import Profile, Question, Answer, Tag
from AskKozlovApp.forms import LoginForm, SignupForm, QuestionForm, SettingsForm, AnswerForm


# Create your views here.


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    iterators = paginator.get_page(page)
    return iterators


def new_questions(request):
    request.session['continue'] = reverse('new questions')
    iterators = paginate(Question.objects.get_new_questions(), request, 5)
    return render(request, 'newquestions.html', {'BestTags': Tag.objects.get_popular(6),
                                                 'BestUsers': Profile.objects.get_best(6), 'iterators': iterators})


def hot_questions(request):
    request.session['continue'] = reverse('hot questions')
    iterators = paginate(Question.objects.get_hot_questions(), request, 5)
    return render(request, 'hotquestions.html', {'BestTags': Tag.objects.get_popular(6),
                                                 'BestUsers': Profile.objects.get_best(6), 'iterators': iterators})


def list_with_tags(request, tg):
    request.session['continue'] = reverse('tag', args=[tg])
    iterators = paginate(Question.objects.get_questions_by_tag(tg), request, 5)
    return render(request, 'tag.html', {'BestTags': Tag.objects.get_popular(6),
                                        'BestUsers': Profile.objects.get_best(6),
                                        'iterators': iterators,
                                        'header': tg})


def signup(request):
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(data=request.POST)
        if form.is_valid():
            try:
                profile = Profile.objects.create(user=User.objects.create_user(form.cleaned_data['login'],
                                                                               form.cleaned_data['email'],
                                                                               form.cleaned_data['password']),
                                                 nickname=form.cleaned_data['nickname'],
                                                 userPfp=form.cleaned_data['user_pfp'])
                if profile is not None:
                    auth.login(request, profile.user)
                    return redirect(reverse('new questions'))
                else:
                    form.add_error('login', 'User already exists')
            except IntegrityError as e:
                if e.args[0] == 'UNIQUE constraint failed: auth_user.username':
                    form.add_error('login', 'User already exists')
                elif e.args[0] == 'UNIQUE constraint failed: auth_user.email':
                    form.add_error('email', 'The email is already registered')

    return render(request, "registration.html", {'BestTags': Tag.objects.get_popular(6),
                                                 'BestUsers': Profile.objects.get_best(6),
                                                 'form': form, })


def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            try:
                if user is not None and user.profile is not None:
                    auth.login(request, user)
                    return redirect(request.session.pop('continue', '/new/'))
                else:
                    form.add_error('password', "Wrong login or password")
            except:
                form.add_error('password', "Wrong login or password")

    return render(request, "login.html", {'BestTags': Tag.objects.get_popular(6),
                                          'BestUsers': Profile.objects.get_best(6),
                                          'form': form})


# for now, it is just link to main page
def logout(request):
    next_url = request.session.pop('continue', '/new/')
    auth.logout(request)
    return redirect(next_url)


@login_required()
def settings(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = SettingsForm(data=request.POST)
        if form.is_valid():
            profile.nickname = form.cleaned_data['nickname']
            profile.userPfp = form.cleaned_data['user_pfp']
            profile.user.username = form.cleaned_data['login']
            profile.user.email = form.cleaned_data['email']
            profile.user.save()
            profile.save()
            return render(request, "settings.html", {'BestTags': Tag.objects.get_popular(6),
                                                     'BestUsers': Profile.objects.get_best(6),
                                                     'form': form, })
        else:
            form.add_error(None, 'General Error')

    data = {'login': profile.user.username,
            'email': profile.user.email,
            'nickname': profile.nickname, }
    form = SettingsForm(data=data)
    return render(request, "settings.html", {'BestTags': Tag.objects.get_popular(6),
                                             'BestUsers': Profile.objects.get_best(6),
                                             'form': form, })


@login_required()
def ask(request):
    request.session['continue'] = reverse('new question')
    if request.method == 'POST':
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            new_question = Question.objects.create(title=form.cleaned_data['title'], fk_profile=request.user.profile)
            new_question.fk_tags.set(form.cleaned_data['tags'])
            new_question.save()
            return redirect(reverse('question', args=[new_question.pk]))
        else:
            return redirect(reverse('new questions'))

    form = QuestionForm
    return render(request, "newquestion.html", {'BestTags': Tag.objects.get_popular(6),
                                                'BestUsers': Profile.objects.get_best(6),
                                                'form': form, })


def question(request, qid: int):
    the_question = Question.objects.get_question_by_id(qid)
    iterators = paginate(Answer.objects.get_by_question_id(qid), request, 5)
    request.session['continue'] = reverse('question', args=[the_question.pk])

    if request.method == 'GET':
        form = AnswerForm
    else:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = Answer.objects.create(text=form.cleaned_data['text'], fk_profile=request.user.profile,
                                           fk_question=the_question)
            page = iterators.end_index()
            return redirect(reverse('question', args=[the_question.pk]) + '?page=' + str(page) + '#'
                            + str(answer.pk))

    return render(request, "question.html", {'BestTags': Tag.objects.get_popular(6),
                                             'BestUsers': Profile.objects.get_best(6),
                                             'isAsker': request.user.pk == the_question.fk_profile.pk,
                                             'question': the_question,
                                             'iterators': iterators,
                                             'form': form, })
