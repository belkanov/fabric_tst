from django.core.management.base import BaseCommand

from authapp.models import User


class Command(BaseCommand):
    help = 'Создает немного пользователей, чтобы было. Только для разработки, не использовать на ПРОДе'

    # для создания юзеров на проде можно написать другую команду, которая, например из файла, создаст нужных.
    def handle(self, *args, **options):
        print('Creating some users... ', end='')
        super_user = User.objects.create_superuser(username='admin', email='mail@example.com', password='123')
        user_1 = User.objects.create_user(username='user_1', password='111')
        user_2 = User.objects.create_user(username='user_2', password='222')
        print('DONE')
