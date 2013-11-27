# newslint-server

## Stuff Used

* [Django](https://www.djangoproject.com/)
* [Bower](https://github.com/bower/bower)
* [Django-Bower](https://django-bower.readthedocs.org/en/latest/)
* [git](http://git-scm.com/)
* [jQuery](http://jquery.com/)
* [momentjs](http://momentjs.com/)
* [celery](http://www.celeryproject.org/)
* [redis](http://redis.io/)
* [font-awesome](http://fontawesome.io/)

## Install

    git clone git@github.com:Xeus/newslint-server.git
    npm install -g bower
    sudo pip install -r requirements.txt
    python manage.py bower_install
    python manage.py migrate

## Start Server

    python manage.py runserver

## TODO

* configure static files
* unit tests
* logging
* make safe default `settings.py`