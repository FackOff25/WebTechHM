from django.contrib import admin
from AskKozlovApp.models import Question, Answer, Tag, Profile, QuestionRatingMark, AnswerRatingMark

# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(QuestionRatingMark)
admin.site.register(AnswerRatingMark)
