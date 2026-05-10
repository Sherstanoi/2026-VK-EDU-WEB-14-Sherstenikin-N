# VK-web-course-1sem
Сайт запускается с помощью команды: docker compose up --build -d

Если вы хотите заполинить сайт данными, то запустите:
docker compose up --build -d
docker compose exec web python manage.py fill_db 10
(вместо 10 можно поставить любое число)

Если нужно создать суперпользователя для провекрки данных в админке, то введите команду:
docker compose exec web python manage.py createsuperuser

Далее нужно перейти в браузере по адреcу http://localhost:8000


Сайт состоит из нескольких страниц:

1. главная страница (новые вопросы) — `/`
   
2. лучшие вопросы — `/hot/`
   
3. вопросы по тегу — `/tag/<имя_тега>/`
   
4. страница вопроса со списком ответов — `/question/<id>/`
   
5. создание вопроса — `/newQuestion`
   
6.  вход — `/login`
   
7.  регистрация — `/register`
    
8.  настройки профиля — `/settings`
    
9.  админка — `/admin/`