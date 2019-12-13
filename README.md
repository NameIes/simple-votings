
## Что нужно сделать перед первым запуском проекта?

1. Создать виртуальное окружение (пожалуйста, не добавляйте его в репу!)

        virtualenv -p python3 venv
        source venv/bin/activate
        pip3 install django
    
2. Зайти в проект и накатить стандартные миграции

        cd simple_votings
        python3 manage.py migrate
    
## Второй и последующие запуски
    source venv/bin/activate
    cd simple_votings
    python3 manage.py runserver
    