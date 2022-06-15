from django.db import models
from django.db.models import ObjectDoesNotExist, signals
from django.http import Http404
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

class ProfileManager(models.Manager):
    def get_best(self, amount):
        try:
            best = self.all()[0:amount]
        except ObjectDoesNotExist:
            raise Http404
        return best


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    nickname = models.CharField(max_length=255, default=None, null=True)
    userPfp = models.ImageField(max_length=255, default=None, null=True, upload_to='avatar/%Y/%m/%d')
    objects = ProfileManager()

    def __str__(self):
        if self.user.username == '':
            return "ERROR-LOGIN IS NULL"
        return self.user.username

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    @property
    def nick(self):
        if self.nickname == '':
            return self.user.username
        else:
            return self.nickname

    @property
    def userlink(self):
        return "/user/" + self.user.username


class TagManager(models.Manager):

    def get_by_question(self, question):
        try:
            answers = self.all().prefetch_related('question_set').filter(question=question)
        except ObjectDoesNotExist:
            raise Http404
        return answers

    def get_popular(self, amount):
        try:
            tags = self.all()[0:amount]
        except ObjectDoesNotExist:
            raise Http404
        return tags


class Tag(models.Model):

    def __str__(self):
        if self.tagname == '':
            return "ERROR-TAG NAME IS NULL"
        return self.tagname

    tagname = models.CharField(primary_key=True, max_length=255)

    objects = TagManager()

    @property
    def link(self):
        return "/tags/" + self.tagname

    class Meta:
        db_table = 'tags'
        managed = True
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class QuestionManager(models.Manager):
    def get_new_questions(self):
        return self.select_related().order_by("-date").prefetch_related('fk_profile', 'fk_tags')

    def get_hot_questions(self):
        return self.select_related().order_by("-rating").prefetch_related('fk_profile')

    def get_questions_by_tag(self, tag):
        questions = self.filter(fk_tags__tagname__iexact=tag).order_by("-rating").prefetch_related('fk_profile')
        if not questions:
            raise Http404
        return questions

    def get_question_by_id(self, pk):
        try:
            questions = self.prefetch_related('fk_profile', 'fk_tags').get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        return questions


class Question(models.Model):

    def __str__(self):
        if self.title == '':
            return "ERROR-QUESTION TITLE IS NULL"
        return self.title

    objects = QuestionManager()

    fk_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    fk_tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)
    answers_num = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    @property
    def link(self):
        return "/question/" + str(self.id) + "/"

    class Meta:
        db_table = 'questions'
        managed = True
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class AnswerManager(models.Manager):
    def get_new(self):
        return self.all().order_by('-date').prefetch_related('user')

    def get_by_question_id(self, q_id):
        try:
            answers = self.all().filter(fk_question=q_id).order_by("-rating").prefetch_related('fk_profile')
        except ObjectDoesNotExist:
            raise Http404
        return answers

    def bulk_create(items, objs):
        super().bulk_create(objs)
        for i in objs:
            post_save.send(i.__class__, instance=i, created=True)


class Answer(models.Model):

    def __str__(self):
        if self.text is None:
            return "ERROR-ANSWER TEXT IS NULL"
        return self.text[:255]

    class Meta:
        db_table = 'answers'
        managed = True
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    objects = AnswerManager()

    fk_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    fk_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    rating = models.IntegerField(default=0)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    marked_correct = models.BooleanField(default=False)


def create_answer(sender, instance, created, **kwargs):
    if created:
        instance.fk_question.answers_num += 1
        instance.fk_question.save()


signals.post_save.connect(receiver=create_answer, sender=Answer)


class QuestionRatingMarkManager(models.Manager):
    def bulk_create(items, objs, size):
        super().bulk_create(objs, size)
        for i in objs:
            post_save.send(i.__class__, instance=i, created=True)

    def get_vote(self, question_id, profile_id):
        votes = {0: 'none', 1: 'up', -1: 'down'}
        mark = self.all().filter(fk_question=question_id, fk_profile=profile_id)
        if mark:
            return votes[mark[0].vote]
        else:
            return votes[0]


class QuestionRatingMark(models.Model):
    votes = [(1, 'up'), (-1, 'down'), (0, 'none'), ]
    objects = QuestionRatingMarkManager()

    vote = models.IntegerField(choices=votes, default=0)
    fk_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    fk_question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.fk_question.title + '-' + self.fk_profile.user.username + ': ' + str(self.vote)

    class Meta:
        verbose_name = 'Q-VoteMark'
        verbose_name_plural = 'Q-VoteMarks'
        unique_together = ['fk_profile', 'fk_question']


def create_question_rating_mark(sender, instance, created, **kwargs):
    if created:
        instance.fk_question.rating += instance.vote
        instance.fk_question.save()


signals.post_save.connect(receiver=create_question_rating_mark, sender=QuestionRatingMark)


class AnswerRatingMarkManager(models.Manager):
    def bulk_create(items, objs, size):
        super().bulk_create(objs, size)
        for i in objs:
            post_save.send(i.__class__, instance=i, created=True)

    def get_vote(self, answer_id, profile_id):
        votes = {0: 'none', 1: 'up', -1: 'down'}
        mark = self.all().filter(fk_question=answer_id, fk_profile=profile_id)
        if mark:
            return votes[mark[0].vote]
        else:
            return votes[0]


class AnswerRatingMark(models.Model):
    votes = [(1, 'up'), (-1, 'down'), (0, 'none'), ]
    objects = AnswerRatingMarkManager()

    vote = models.IntegerField(choices=votes, default=0)
    fk_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    fk_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.fk_answer.text[:10] + '-' + self.fk_profile.user.username + ': ' + str(self.vote)

    class Meta:
        verbose_name = 'A-VoteMark'
        verbose_name_plural = 'A-VoteMarks'
        unique_together = ['fk_profile', 'fk_answer']


def create_answer_rating_mark(sender, instance, created, **kwargs):
    if created:
        instance.fk_answer.rating += instance.vote
        instance.fk_answer.save()


signals.post_save.connect(receiver=create_answer_rating_mark, sender=AnswerRatingMark)
