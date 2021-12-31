from django.conf import settings
from rest_framework.serializers import StringRelatedField, ModelSerializer, IntegerField

from .models import Quiz, Question, PossibleAnswer, UserAnswer


class QuizModelSerializer(settings.ENV_MODEL_SERIALIZER):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizUpdateSerializer(QuizModelSerializer):
    class Meta:
        model = Quiz
        exclude = ('start_date',)


class QuestionModelSerializer(settings.ENV_MODEL_SERIALIZER):
    class Meta:
        model = Question
        fields = '__all__'


class PossibleAnswerModelSerializer(settings.ENV_MODEL_SERIALIZER):
    class Meta:
        model = PossibleAnswer
        fields = '__all__'


class UserAnswerModelSerializer(settings.ENV_MODEL_SERIALIZER):
    class Meta:
        model = UserAnswer
        exclude = ('answered_by',)

    def create(self, validated_data):
        validated_data['answered_by'] = self.context['request'].user
        return super().create(validated_data)


# class AnsweredSerializer
class AnsweredSerializer(ModelSerializer):
    answered_by = StringRelatedField()
    possible_answer = StringRelatedField()
    possible_answer_id = IntegerField(source='possible_answer.pk')
    question_id = IntegerField(source='possible_answer.question.pk')
    quiz_id = IntegerField(source='possible_answer.question.quiz.pk')

    class Meta:
        model = UserAnswer
        fields = '__all__'
