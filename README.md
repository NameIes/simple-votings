
## Что нужно сделать перед первым запуском проекта?

1. Создать виртуальное окружение (пожалуйста, не добавляйте его в репу!)

        virtualenv -p python3 venv
        source venv/bin/activate
        pip3 install django
    
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
