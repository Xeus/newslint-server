# newslint-server

A little project to lint a block of text to see how newsworthy, objective, sensationalist, pundit-prone, etc. it is.  It comes from my interest in reading the news and identifying political bait.  And it was enabled by the excellent joblint project originally done in JavaScript by [Rowan Manning](https://github.com/rowanmanning/joblint).

I wanted to port Rowan's code to Python first, then give it a Django server backend to interface with over the web so I could learn Django.  I wanted to use Django's views and templates but also build an API so I could build it a second way with a RESTful interface, potentially using Ember.js so I could learn that too.

The Python port of joblint is at https://github.com/Xeus/joblint_python while my newslinter is at https://github.com/Xeus/newslint in case you want to check them out too.

My other goals were to write Django tests (I didn't know enough Django to try TDD since I had to learn every step as I went) and to build a solid Grunt-enabled development environment using SASS, which I'd also never used before.

And if all went well, I wanted to add in celery tasks so I could scrape a URL and serve up the results later.

So basically this is a testbed site to learn lots of stuff.  Hope it's useful to someone else too!

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
* [autoprefixer](https://github.com/ai/autoprefixer)
* [SASS](http://sass-lang.com/)
* [Compass](http://compass-style.org/)

## Install

You might need these installed:

    sudo curl https://npmjs.org/install.sh | sh
    sudo npm install -g bower
    sudo gem update --system
    sudo gem install compass
    sudo gem install sass

Set up repo:

    git clone git@github.com:Xeus/newslint-server.git
    sudo pip install -r requirements.txt
    python manage.py bower_install
    npm install
    grunt build
    python manage.py syncdb

## Start Server

    python manage.py runserver

## Tests

    python manage.py test linter

## TODO

* logging
* make safe default `settings.py`
* celery for scraping a url
* front-end design
