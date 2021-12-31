from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Quiz, Question, PossibleAnswer, UserAnswer
from .serializers import QuizModelSerializer, QuizUpdateSerializer, QuestionModelSerializer, PossibleAnswerModelSerializer, UserAnswerModelSerializer, AnsweredSerializer


# либо можно использовать встроенный IsAdminUser,
# если под админом системы имелся ввиду пользователь с флагом is_stuff
#
# если так, то надо будет еще группу создать и выдать им права на редактирование,
# т.к. по дефолту все могут только смотреть

# class IsSuperUser(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_superuser)


class QuizModelViewSet(ModelViewSet):
    # renderer_classes = [CamelCaseJSONRenderer]  # можно добавить для нативных имен в JS
    queryset = Quiz.objects.all()

    def get_queryset(self):
        quizzes = Quiz.get_base_filtered(self.request.user.is_superuser, self.request.query_params.get('quiz'))
        return quizzes

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return QuizUpdateSerializer
        else:
            return QuizModelSerializer

    # на случай использования is_active - отключать можно тут
    # def perform_destroy(self, instance):
    #     instance.is_active = False
    #     instance.save()


class QuestionModelViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionModelSerializer

    def get_queryset(self):
        quizzes = Quiz.get_base_filtered(self.request.user.is_superuser, self.request.query_params.get('quiz'))
        questions = Question.objects.filter(quiz_id__in=quizzes)
        return questions


class PossibleAnswerModelViewSet(ModelViewSet):
    queryset = PossibleAnswer.objects.all()
    serializer_class = PossibleAnswerModelSerializer

    def get_queryset(self):
        quizzes = Quiz.get_base_filtered(self.request.user.is_superuser, self.request.query_params.get('quiz'))
        questions = PossibleAnswer.objects.filter(question__quiz_id__in=quizzes)
        return questions


class UserAnswerModelViewSet(ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerModelSerializer

    def get_queryset(self):
        is_superuser = self.request.user.is_superuser
        quizzes = Quiz.get_base_filtered(is_superuser, self.request.query_params.get('quiz'))
        user_answers = UserAnswer.objects.filter(possible_answer__question__quiz_id__in=quizzes)
        if is_superuser:
            if user_id := self.request.query_params.get('user'):
                user_answers = user_answers.filter(answered_by=user_id)
        elif self.request.user.is_authenticated:
            user_answers = user_answers.filter(answered_by=self.request.user)
        else:
            user_answers = UserAnswer.objects.none()
        return user_answers


class AnsweredViewSet(ListAPIView):
    # queryset = UserAnswer.objects.all()
    serializer_class = AnsweredSerializer

    def get_queryset(self):
        user_answers = UserAnswer.objects.all()
        if self.request.user.is_superuser:
            if answered_by := self.kwargs.get('pk'):
                user_answers = user_answers.filter(answered_by=answered_by)
        elif self.request.user.is_authenticated:
            user_answers = user_answers.filter(answered_by=self.request.user)
        else:
            user_answers = UserAnswer.objects.none()
        return user_answers
