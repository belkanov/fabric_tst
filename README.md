# fabric_tst
Насколько я понял - реализация довольно вольная, поэтому вот несколько моментов по поводу кода:
 - много всяких "если". Из-за этого много ВОЗМОЖНЫХ проверок/реализаций. Я не стал в
   них углубляться.
 - анонимно =/= без авторизации. Поэтому для анонимного ответа логинимся под
   anonymous/anonymous. К такой схеме можно привязать готовые токены авторизации, 
   которые можно рассылать пользовтелям по почте, например. Ну или не токены, а 
   какиенить метрики. Так с одной стороны мы получим анонимные ответы, а с другой 
   можно гарантировать, что один пользователь пройдет опрос один раз (после 
   прохождения удалить токен и все, само собой анонимусу сделать пароль посложнее 
   чем текущий, ну или как-то по другому организовать)
 - нет проверок на корректный ответ. Т.е. если вдруг вопрос преполагает один ответ 
   из многих, все равно можно добавить несколько ответов (тут надо либо делать 
   проверку, либо отдать это на откуп фронту/клиенту, чтобы он смотрел на тип 
   вопроса)
 - я считаю неккорректным возможность смотреть ответы других пользователей, поэтому 
   ответы фильтруются по залогиненому (админ - исключение и видит все, конечно ему 
   можно выдавать ответы предварительно обзлечивия: в духе есть ответ на вопрос или 
   нет, но это опять "если", которым я заниматься не стал). Конечно это можно поменять на запрос по ID (как и писалось в ТЗ). Я бы такие моменты обсуждал с заказчиком. Тут связи с заказчиком нет, поэтому оставил на свое усмотрение.
 - админ может фильтровать ответы по пользователям (это переезд фильтрации по ИД 
   пользователя из функционала пользователя ввиду пункта выше)  
 - опросы, вопросы, варианты и ответы можно фильтровать по опросу
 - ответ все равно можно добавить, если опрос закончился по времени. Тут опять либо 
   проверка, либо фронт сначала получает список активных опросов и уже по нему 
   работает дальше.
 - метод GET в user-answers в принципе лишний. Я не стал его отключать - т.к. это 
   удобно для отладки и просмотра (если вдруг будете запсукать). 
   Если прям очень надо будет отключить - можно, например, вручную описать методы в 
   регистрации роутера. Можно переопределить метод во вьюсете, ну или переделать 
   вьюсет на что-то свое с миксинами. Варианты найдутся. В существующем проекте 
   конечно есть смысл делать как уже принято. В том числе возможно реализацию делать 
   через FBV, а не CBV. "Если"...
 - строгих ограничений в ТЗ я не увидел, поэтому есть такие вольности как 
   DELETE/PATCH у ответов пользователя. По этим же причинам - остались висеть лишние 
   методы (как GET выше). Тут можно добавить проверку, что нельзя удалять ответы у 
   полностью пройденных опросов. Или их вообще нельзя удалять. Или можно только 
   править.
 - админ системы - суперюзер. Так было проще с выдачей всех прав.
   Если надо прям группу админов - это можно сделать в процессе выдаи базовых прав в 
   команде authapp.create_base_permissions
 - `__str__` у моделей для наглядности и быстроты отладки. Само собой можно отключить 
   для прода или изначально не выводить.
 - получение пройденных опросов превратилось в получение записанных ответов. Заметил 
   это под конец - переделывать не стал. Информация получилась с избытком (
   дублирование ИД опроса например). Конечно можно переделать.
 - poetry не настраивал (я про версии, URL, ...)
 - добавил db.sqlite3 намеренно, чтобы можно было посмотреть немного локально.
 - не делал HTTPS
 - отдельный пункт в виде документации по API смотрится как прям ручное
   документирование, поэтому swagger опустил, хотя подозреваю, что зря.

В общем много "если"...

# API
## общие положения
 - для опросов, вопросов, вариантов ответов, ответов пользователя работает фильтр вида: ?quiz=2
 - для пользователей идет фильтрация по доступным опросам (дата окончания >= текущей дате)
## Логин
http://127.0.0.1:8888/api/token-auth/

POST
{
    "username": "anonymous",
    "password": "anonymous"
}

->

{
    "token": "0462fd4639eba12506510628c25b7ce5bb232a16"
}

## Опросы 

### все опросы
http://127.0.0.1:8888/api/quizzes/

GET ->

    [
        {
            "id": 2,
            "quiz_name": "quiz name 2",
            "quiz_description": "quiz desc 2",
            "start_date": "2021-12-30T22:54:19+05:00",
            "end_date": "2022-12-31T22:54:19+05:00"
        }
    ]

админу доступен POST/PUT для этого и других API.
Для этого дата не обязательна (дефолт: текущее время +1 час, время проведения - сутки).
start_date можно отсылать повторно, но эффекта не будет

### конкретный опрос
http://127.0.0.1:8888/api/quizzes/:id/

GET ->

    {
        "id": 2,
        "quiz_name": "quiz name 2",
        "quiz_description": "quiz desc 2",
        "start_date": "2021-12-30T22:54:19+05:00",
        "end_date": "2022-12-31T22:54:19+05:00"
    }

## вопросы (аналогия с опросами)
http://127.0.0.1:8888/api/questions/

    [
        {
            "id": 1,
            "quiestion_text": "вопрос 1",
            "question_type": 1,
            "quiz": 1
        },
        ...
        {
            "id": 6,
            "quiestion_text": "вопрос 3",
            "question_type": 3,
            "quiz": 2
        }
    ]


"question_type": 1, - ответ текстом
"question_type": 2, - выбор одного варианта из нескольких
"question_type": 3, - выбор нескольких вариантов

## возможные ответы (аналогия с опросами)
http://127.0.0.1:8888/api/possible-answers/


    [
        {
            "id": 1,
            "answer_text": "свой вариант",
            "question": 1
        },
        ...
        {
            "id": 3,
            "answer_text": "опция 2",
            "question": 2
        }
    ]    

## записанные ответы пользователя (аналогия с опросами)
http://127.0.0.1:8888/api/user-answers/

## записать ответ
http://127.0.0.1:8888/api/user-answers/

POST
Headers:
{
  "Content-Type": "application/json",
  "Authorization": "Token 4c20d7154b541fec5fee920c1720f372756e8486"
}

Payload:
{
  "text": 222,
  "possible_answer": 12
}

текст не обязателен. Имеет смысл когда тип вопроса (question_type) указан как ответ текстом (1)


## пройденные опросы:
http://127.0.0.1:8888/api/answered/

    [
        {
            "id": 1,
            "answered_by": "user_2",
            "possible_answer": "[2] [4] [8] свой вариа...",
            "possible_answer_id": 8,
            "question_id": 4,
            "quiz_id": 2,
            "text": "ответ ответ"
        },
        ...
        {
            "id": 5,
            "answered_by": "user_2",
            "possible_answer": "[2] [6] [12] опция 14...",
            "possible_answer_id": 12,
            "question_id": 6,
            "quiz_id": 2,
            "text": "222"
        }
    ]

для конкретного пользователя (работает только для админа, остальным - фильтрует по себе)
http://127.0.0.1:8888/api/answered/:user_id/

# INSTALL

Считаю, что Debian 11, есть права рута (или sudo где требуется), стоят нужные обновы.

```
apt install nginx
apt install postgresql postgresql-contrib
apt install git-core

pip install poetry
```


```
useradd -g www-data -m django
cd /home/django/

git clone git@github.com:belkanov/fabric_tst.git

cd fabric_test

poetry install
poetry env info
```

тут получим вывод вида
```
Virtual environment
Python:         3.7.1
Implementation: CPython
Path:           /path/to/poetry/cache/virtualenvs/test-O3eWbxRl-py3.7
Valid:          True

System
Platform: darwin
OS:       posix
Python:   /path/to/main/python
```

нас интересует строчка Path. запомним.

Далее добавляем gunicorn (т.к. мы больше не создавали новых српед в poetry - перехода в текущий каталог достаточно для активации среды)

```
poetry add gunicorn

python3 manage.py migrate
python3 manage.py runserver
```
на этом этапе должно появится обычное сообщение, что серв стартанул.

Работаем дальше с настройками:

```
chown -R django /home/django/
chmod -R 755 /home/django/fabric_test/

nano /etc/systemd/system/gunicorn.service
```

в нем (внимание на путь, вспоминаем Path выше):
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=django
Group=www-data
WorkingDirectory=/home/django/fabric_test
ExecStart=/path/to/poetry/cache/virtualenvs/test-O3eWbxRl-py3.7/bin/gunicorn --access-logfile --workers 3 --bind unix:/home/django/fabric_test/fabric_test.sock fabric_test.wsgi

[Install]
WantedBy=multi-user.target
```

сохраняем.

Далее:
```
systemctl enable gunicorn
systemctl start gunicorn
systemctl status gunicorn
```

После того, как сервис успешно запустился, можно настроить параметры для nginx, для этого необходимо создать новый файл и внести в него конфигурацию:
```
nano /etc/nginx/sites-available/fabric_test
```

в нем (server_name - IP сервера):
```
server {
    listen 80;
    server_name 151.248.117.226;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/django/fabric_test;
    }

    location /media/ {
        root /home/django/fabric_test;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/django/fabric_test/fabric_test.sock;
    }
}
```

сохраняем и далем его активным:
```
ln -s /etc/nginx/sites-available/fabric_test /etc/nginx/sites-enabled
```

Проверяем настройки «nginx»:
```
nginx -t
```

Перезапускаем службу «nginx» и добавляем разрешения в сетевой экран:
```
systemctl restart nginx
```

Если все ОК - поздравляю, Вы великолепны.