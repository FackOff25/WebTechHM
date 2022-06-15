from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse

from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods

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


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(data=request.POST)
        if form.is_valid():
            try:
                form.save()
                if form.instance is not None:
                    auth.login(request, form.instance.user)
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


@require_http_methods(['GET', 'POST'])
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
@require_http_methods(['GET', 'POST'])
def settings(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        initial_data = request.POST.copy()
        form = SettingsForm(data=initial_data, instance=request.user, files=request.FILES)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect(reverse('settings'))

    data = {'login': profile.user.username,
            'email': profile.user.email,
            'nickname': profile.nickname,
            'avatar': profile.userPfp}
    form = SettingsForm(data=data)
    return render(request, "settings.html", {'BestTags': Tag.objects.get_popular(6),
                                             'BestUsers': Profile.objects.get_best(6),
                                             'form': form, })


@login_required()
@require_http_methods(['GET', 'POST'])
def ask(request):
    request.session['continue'] = reverse('new question')
    if request.method == 'POST':
        form = QuestionForm(data=request.POST, instance=Question(request.POST))
        if form.is_valid():
            form.save({'user': request.user, })
            return redirect(reverse('question', args=[form.instance.pk]))
        else:
            return redirect(reverse('new questions'))

    form = QuestionForm
    return render(request, "newquestion.html", {'BestTags': Tag.objects.get_popular(6),
                                                'BestUsers': Profile.objects.get_best(6),
                                                'form': form, })


@require_http_methods(['GET', 'POST'])
def question(request, qid: int):
    the_question = Question.objects.get_question_by_id(qid)
    iterators = paginate(Answer.objects.get_by_question_id(qid), request, 5)
    request.session['continue'] = reverse('question', args=[the_question.pk])

    if request.method == 'GET':
        form = AnswerForm
    else:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            form.save({'user': request.user, 'question': the_question, })
            # redirect
            answers_list = Paginator(Answer.objects.get_by_question_id(qid), 5)
            needed_page = iterators.end_index()
            for i in range(1, answers_list.num_pages + 1):
                if form.instance in answers_list.page(i).object_list:
                    needed_page = i
                    break
            return redirect(reverse('question', args=[the_question.pk]) + '?page=' + str(needed_page) + '#answer-'
                            + str(form.instance.pk))

    return render(request, "question.html", {'BestTags': Tag.objects.get_popular(6),
                                             'BestUsers': Profile.objects.get_best(6),
                                             'isAsker': request.user.pk == the_question.fk_profile.pk,
                                             'question': the_question,
                                             'iterators': iterators,
                                             'form': form, })
