# newslint-server

A little project to lint a block of text to see how newsworthy, objective, sensationalist, pundit-prone, etc. it is.  It comes from my interest in reading the news and identifying political bait.  And it was enabled by the excellent joblint project originally done in JavaScript by [Rowan Manning](https://github.com/rowanmanning/joblint).

I wanted to port Rowan's code to Python first, then give it a Django server backend to interface with over the web so I could learn Django.  I wanted to use Django's views and templates but also build an API so I could build it a second way with a RESTful interface, potentially using Ember.js so I could learn that too.

The Python port of joblint is at https://github.com/Xeus/joblint_python while my newslinter is at https://github.com/Xeus/newslint in case you want to check them out too.

My other goals were to write Django tests and analyze them with `coverage` (I didn't know enough Django to try TDD since I had to learn every step as I went) and to build a solid Grunt-enabled development environment using SASS, which I'd also never used before.

I tried to deploy this to Amazon Elastic Beanstalk but ran into complications (git submodules, django pathing, static files from grunt, local/production settings) so I set it up on an EC2 server behind memcache, Varnish, and Apache instead.

In the future, if things go well, I hope to add in celery tasks so I could scrape a URL and serve up the results later.

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

    sudo add-apt-repository ppa:chris-lea/node.js
    curl http://repo.varnish-cache.org/debian/GPG-key.txt | sudo apt-key add -
    echo "deb http://repo.varnish-cache.org/ubuntu/ precise varnish-3.0" | sudo tee -a /etc/apt/sources.list
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install apache2 python-setuptools libapache2-mod-wsgi python-pip sqlite3 libsqlite3-dev php5 libapache2-mod-php5 varnish python-software-properties nodejs rubygems build-essential git mysql-server mysql-client libmysqlclient-dev python-dev
    wget https://dl-ssl.google.com/dl/linux/direct/mod-pagespeed-stable_current_amd64.deb
    sudo dpkg -i mod-pagespeed-*.deb
    sudo apt-get -f install
    sudo service apache2 restart
    sudo curl https://npmjs.org/install.sh | sudo sh
    sudo npm cache clean -f
    sudo npm install -g n grunt-cli bower forever
    sudo n stable
    wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | sudo python
    sudo easy_install -U distribute
    sudo gem update
    sudo gem install compass
    sudo gem install sass

Set up repo:

    git clone git@github.com:Xeus/newslint-server.git
    sudo pip install -r requirements.txt
    python manage.py bower_install
    npm install
    grunt build
    python manage.py syncdb
    cd linter/lib
    git clone git@github.com:Xeus/newslint.git

## Start Server

If you're running it locally, do this from the `app/` directory.

    cd ~/app
    python manage.py runserver

If on a remote or staging server, you're probably using Apache.

In `/etc/apache2/sites-enabled/staging`, make sure your specific site includes the following:

    <VirtualHost *:80>
        ServerName localhost
        WSGIScriptAlias / /home/ubuntu/app/newslint/wsgi.py

        <Directory /home/ubuntu/app/newslint>
            <Files wsgi.py>
                Order deny,allow
                Require all granted
            </Files>
        </Directory>

        <IfModule mod_expires.c>
            <FilesMatch "\.(jpg|gif|png|css|js|map)$">
                ExpiresActive on
                ExpiresDefault "access plus 7 days"
            </FilesMatch>
        </IfModule>

        <LocationMatch "\.(pdf|ico)$">
            SetHandler None
        </LocationMatch>
        Alias /favicon.ico /home/ubuntu/app/static/build/img/favicon.ico
        Alias /static /home/ubuntu/app/static

        <Directory /home/ubuntu/app/static>
            Order allow,deny
            Require all granted
            Allow from all
        </Directory>
        <Location /git_pull>
            Satisfy any
            Allow from 192.30.252.0/22 127.0.0.1
        </Location>
    </VirtualHost>

## Tests

    python manage.py test linter

## TODO

* logging needs to save somewhere
* celery for scraping a url (install redis where?)
* mobile spacing, header spacing, footer spacing
