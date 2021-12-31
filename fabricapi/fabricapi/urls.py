from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_authtoken
from quizapp.views import QuizModelViewSet, QuestionModelViewSet, PossibleAnswerModelViewSet, UserAnswerModelViewSet, AnsweredViewSet
from django.conf import settings

router = DefaultRouter()
router.register('quizzes', QuizModelViewSet)
router.register('questions', QuestionModelViewSet)
router.register('possible-answers', PossibleAnswerModelViewSet)
router.register('user-answers', UserAnswerModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),
    path('api/answered/', AnsweredViewSet.as_view()),
    path('api/answered/<int:pk>/', AnsweredViewSet.as_view()),
    path('api/token-auth/', rest_authtoken.obtain_auth_token),
]

if settings.DEBUG:
    urlpatterns.extend([
        path('api/auth/', include('rest_framework.urls')),
    ])
