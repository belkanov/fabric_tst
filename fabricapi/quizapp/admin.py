from django.contrib import admin

from .models import Quiz, Question, PossibleAnswer, UserAnswer

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(PossibleAnswer)
admin.site.register(UserAnswer)
