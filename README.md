
## Что нужно сделать перед первым запуском проекта?

1. Создать виртуальное окружение (пожалуйста, не добавляйте его в репу!)

        virtualenv -p python3 venv
        source venv/bin/activate
        pip3 install django
        pip3 install Pillow
        pip3 install django-crispy-forms
    
2. Зайти в проект и накатить стандартные миграции

        cd simple_votings
        python3 manage.py migrate
    
## Второй и последующие запуски

  * Активируйте виртуальную среду:
  
        source venv/bin/activate
	
  *  Перейдите в каталог:

         cd simple_votings
  
  *  Если вы меняли файл models.py:

         python mange.py makemigrations
         python mange.py migrate
  
  * Запустите сервер разработки:

        python manage.py runserver

  
## Как создать администратора

После шага migrate если у вас нет администратора создайте его командой:

    python manage.py createsuperuser

Надо будет задать имя пользователя, почтц(не реальную он не проверяет) и пароль. Например admin : admin

## Как выгрузить данные приложения и загрузить начальные данные

Создаем бэкап данных приложения

```
python manage.py dumpdata --format=json simple_votings_app > simple_votings_app/fixtures/initial_data.json
```

Удаляем базу, а затем с нуля запускаем создание моделей в ней и в конце создаем суперпользователя и загружаем данные

```
  rm db.sqlite3 
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py loaddata simple_votings_app/initial_data.json 
```

## Если вдруг ничего не работает
Удалите файл db.sqlite3, затем удалите папку migrations в simple_votings_app и введите комманды

    python manage.py makemigrations simple_votings_app
    python manage.py migrate