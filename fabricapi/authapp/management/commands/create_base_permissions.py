from django.contrib.auth.models import Permission, Group
from django.core.management.base import BaseCommand

from authapp.models import User


class Command(BaseCommand):
    help = """
    Создает анонимуса и дает ему прав отвечать.
    К моменту запуска команды предполагается, что проведены миграции (для выдачи прав).
    Еще желательно создать админа, чтобы ИД == 1 не был занят анонимусом и не вызывал диссонанса при просмотре БД.
    """

    def handle(self, *args, **options):
        print('Get/Create anonymous user... ', end='')
        anonymous, created = User.objects.get_or_create(username='anonymous')
        if created:
            anonymous.set_password('anonymous')
            anonymous.save()
        print('DONE')

        print('Get permissions... ', end='')
        add_useranswer_permission = Permission.objects.get(content_type__app_label='quizapp', codename='add_useranswer')
        print('DONE')
        print('Get/Create user group... ', end='')
        answer_user_group, *_ = Group.objects.get_or_create(name='user_answer')
        print('DONE')
        print('Add permissions to the group... ', end='')
        answer_user_group.permissions.add(add_useranswer_permission)
        print('DONE')
        print('Add anonymous to the group... ', end='')
        anonymous.groups.add(answer_user_group)
        print('DONE')

