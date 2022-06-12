from django import template
from AskKozlovApp.models import QuestionRatingMark, AnswerRatingMark

register = template.Library()


@register.filter(name="check_question_vote")
def check_question_vote(value, profile_id):
    return QuestionRatingMark.objects.get_vote(value, profile_id)


@register.filter(name="check_answer_vote")
def check_answer_vote(value, profile_id):
    return AnswerRatingMark.objects.get_vote(value, profile_id)
