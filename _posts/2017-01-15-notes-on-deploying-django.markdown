---
layout: post
title: "170115 - Notes on deploying Django"
date: 2017-01-15 01:17:06
categories: django
---

# Deploy with Ubuntu on Apache

The note below works as of January 2017 and uses Ubuntu 14.04.4 LTS, Apache 2.4, Python 3.4.3, Django 1.10.3, and mod_wsgi 4.5.13. Other versions of any of these softwares might work or not work.

## Step-by-step

1. [Create][create_user] a non-root user account with sudo privilege, and SSH to that non-root account
- [User privilege][linux_user_privilege]

2. Install these packages on Ubuntu:
- python3-pip
- libapache2-mod-wsgi-py3 (this is a binary mod_wsgi compiled with Python 3.4.0, so if you use other versions of Python, e.g. 3.4.!0, 3.!4, mod_wsgi might not work, and it would be better to compile from source - see below)
- libxml2, libxml2-dev, libxlst1.1, libxslt1-dev, libjpeg-turbo8, libjpeg-turbo8-dev, libpng-dev, libfreetype6-dev (these are packages that my Django app requires, you might not need, so you can skip it)

3. Install virtualenv on Ubuntu: `sudo pip3 install virtualenv`

4. Create a new environment: `virtualenv -p python3.4 [env_name]` and activate it (`source activate [env_name]/bin/activate`)

5. Install django (1.10.3): `pip3 install django=1.10.3`, start a test project, migrate, create super user, collect static, and run it with `./manage.py runserver 0.0.0.0:8000`. The test site should show up when connected using the browser to [IP address]:8000.

6. Configure Apache and mod_wsgi:
- Create a text file inside `/etc/apache2/sites-available/`. In this example, let's call it `abc.conf`, and add the following:

{% highlight %}
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
WSGISocketPrefix /var/run/wsgi

<VirtualHost *:80>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    Alias /static /path/to/static/folder
    <Directory /path/to/static/folder/>
            Order allow,deny
            Allow from all
    </Directory>

    <Directory /path/to/your/django/app/folder/>
            Require all granted
    </Directory>

    <Directory /path/to/folder/that/contains/wsgi.py/>
            <Files wsgi.py>
                    Require all granted
            </Files>
    </Directory>

    WSGIDaemonProcess [any_name] python-path=/path/to/your/django/app/folder:/path/to/your/python/site-packages python-home=/path/to/your/virtual/env
    WSGIProcessGroup [any_name]
    WSGIScriptAlias / /path/to/your/wsgi.py
</VirtualHost>
{% endhighlight %}

- Explanation of the above configuration:
    + LoadModule: load mod_wsgi module, so that WSGI directives will be recognized by Apache
    + WSGISocketPrefix: see errors section below
    + ErrorLog, CustomLog: directory where the log files will be stored
    + Alias /static /path/to/static/folder and <Directory ...static/folder>...</Directory>: serve static files, and enable read-write permissions on folder contain static files
    + <Directory .../app/folder/>...</Directory>: allow access the folder that contains all execution files
    + <Directory .../wsig.py/>...</Directory>: allow access to the wsgi.py file
    + WSGIDaemonProcess: basically, the site will be served by a daemon process (anytime Apache receives request that directed to this virtual host, it will pass the request to a wsgi process, this process will execute and return back the result). It will need several arguments, but shown above are
        * the name of daemon process
        * path to your python code, the site-packages that contains all packages that your Python will need (followed by colon)
        * the path to your virtual environment (so that WSGI can run the code with the correct Python version)
    + WSGIProcessGroup: same name as the daemonprocess above
    + WSGIScriptAlias: anything from / (the root domain) will be handled by wsgi.py
- Symlink `abc.conf` to sites-enabled

7. Handle permission issues
- Give Apache access and group ownership to sqlite database
    + `chmod 664 /path/to/db.sqlite3/file`
    + `sudo chown :www-data /path/to/db.sqlite3/file`
- Give Apache group ownership to the Django app files: `sudo chown :www-data /path/to/project`

8. Restart Apache: `sudo service apache2 restart`

## Errors

During installing and configuring mod_wsgi, several errors arise:

#### Mismatch in compiled Python and runtime Python

{% highlight %}
mod_wsgi: Compiled for Python/3.4.0.
mod_wsgi: Runtime using Python/3.4.3.
{% endhighlight %}

and 

{% highlight %}
Exception ignored in: <module 'threading' from '/usr/lib/python3.4/threading.py'>
Traceback (most recent call last):
    File "/usr/lib/python3.4/threading.py", line 1288, in _shutdown
        assert tlock is not None
AssertionError:
{% endhighlight %}

In my case, I use libapache2-mod-wsgi-py3, which is compiled for Python 3.4.0. However, in my environment, I use Python 3.4.3. So I uninstalled libapache2-mod-wsgi-py3 and compile mod_wsgi from source against the correct Python version (more information on compile from source below)

#### Permissions issue

(13)Permission denied: [client ::1:36568] mod_wsgi (pid=14185): Unable to connect to WSGI daemon process '[name_here]' on '/var/run/apache2/wsgi.[...].sock' after multiple attempts

or 

`(13)Permission denied: [client ::1:37840] mod_wsgi (pid=20690): Unable to connect to WSGI daemon process 'cpp_test' on '/var/run/apache2/wsgi.[...].sock' as user with uid=[...].`

Refer [here](http://modwsgi.readthedocs.io/en/develop/user-guides/configuration-issues.html). But the main point is Apache process communicates with WSGI daemon process through UNIX sockets (basically files on disk). If the folder contains those files don't have read/write permission, communication halts. E.g. in the example above Apache cannot read/write on /var/run/apache2. As a result, we need to assign a different location, by:

`WSGISocketPrefix run/wsgi`

Some Linux distributions (including Ubuntu) prohibit read/write on run, so use this instead:

`WSGISocketPrefix /var/run/wsgi`


#### Cannot load mod_wsgi.so

`Cannot load modules/mod_wsgi.so into server: /etc/apache2/modules/mod_wsgi.so: cannot open shared object file: No such file or directory`

This error probably comes from wsgi.conf and wsgi.load not symlinked in mods-enabled. To solve it:
- `sudo a2enmod wsgi`
or 
- `LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so` (in configuration file above)

## Compile from sources

{% highlight %}
wget -q "https://github.com/GrahamDumpleton/mod_wsgi/archive/4.5.13.tar.gz"
tar -xzf '4.5.13.tar.gz'
cd ./mod_wsgi-4.5.13
./configure --with-python=/path/to/the/right/python/executable
make
make install
{% endhighlight %}

Depending on the Apache version that apache2-dev library should be installed - `sudo apt-get install apache2-dev`. Otherwise, during ./configure, something like this might appear `apxs: command not found`

## Conclusion

This note contains information from the following sources:
- [mod_wsgi official documentation][mod_wsgi_doc]
- [How to serve Django applications with Apache and mod_wsgi on Ubuntu 14.04][digital_ocean_tut]
- [Django resources][django_resource]

Other sources:
- This can be an easier way to install [mod_wsgi][mod_wsgi_pip] (haven't tried yet)
- [Set up uwsgi and nginx to serve Python apps on Ubuntu][uwsgi_nginx]
- [How to configure Apache Web Server on an Ubuntu or Debian VPS][apache_ubuntu]

http://stackoverflow.com/questions/2285879/how-do-i-redirect-domain-com-to-www-domain-com-under-django

[create_user](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-14-04#step-one-—-root-login)
[digital_ocean_tut](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04)
[linux_user_privilege](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file-on-ubuntu-and-centos)
[mod_wsgi_doc](http://modwsgi.readthedocs.io/en/develop/user-guides/installation-issues.html)
[mod_wsgi_pip](https://pypi.python.org/pypi/mod_wsgi)
[uwsgi_nginx](https://www.digitalocean.com/community/tutorials/how-to-set-up-uwsgi-and-nginx-to-serve-python-apps-on-ubuntu-14-04)
[apache_ubuntu](https://www.digitalocean.com/community/tutorials/how-to-configure-the-apache-web-server-on-an-ubuntu-or-debian-vps)
[django_resource](https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/modwsgi/)