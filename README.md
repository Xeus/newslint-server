# newslint-server

## Stuff Used

* [Python](http://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Bower](https://github.com/bower/bower)
* [Django-Bower](https://django-bower.readthedocs.org/en/latest/)
* [git](http://git-scm.com/)
* [jQuery](http://jquery.com/)
* [Grunt](http://gruntjs.com/)
* [momentjs](http://momentjs.com/)
* [celery](http://www.celeryproject.org/)
* [redis](http://redis.io/)
* [font-awesome](http://fontawesome.io/)

## Install

You might need these installed:

    curl https://npmjs.org/install.sh | sh
    npm install -g bower

Set up repo:

    git clone git@github.com:Xeus/newslint-server.git
    sudo pip install -r requirements.txt
    python manage.py bower_install
    npm install
    grunt default
    python manage.py migrate

## Start Server

    python manage.py runserver

## TODO

* configure static files
* unit tests
* logging
* make safe default `settings.py`