---
layout: post
title: "Deploying Django to AWS Elastic Beanstalk"
date: 2016-12-02 19:50:12
categories: web
---
Documentation of the steps to deploy Django to EB

1. Freeze pip and export environment to requirements.txt, located in the project root folder

    * Remember not to include unnecessary libraries. They might inadvertantly break the installation (e.g psycorg2 w/o postgre will raise error during installation)

2. Create .ebextensions and include a [whatever].config file:

    * The reference for Python configuration should be [here][python_configuration].

    *   {% highlight python %}
        option_settings:
          aws:elasticbeanstalk:container:python:
            WSGIPath: [path/to/wsgi]
          aws:elasticbeanstalk:application:environment:
            [key: value] of environment variables
          aws:elasticbeanstalk:container:python:staticfiles:
            [url_path: dir_replacement]
        {% endhighlight %}

    * You can edit the configuration any time using `eb config`. This command will fetch the configuration from server and populate it to you vim or whatnot for you to edit.

    * The complete environment configuration can be referred [here][eb_environment_configuration]


3. `eb init` to set up eb cli - server interaction. This step just initializes the information, it does not create anything on the server-side. If you need to change your settings later, run `eb init -i`. The whole idea of this initialization process is to set up your desired server region, ssh key (so that you would be able to access your server using command line).

4. Commit your local repository before the next step (`eb create`), as well as whenever you make a change in your local repository and want to reflect that change on server using `eb deploy`. The idea of EB is to upload the latest commit that you make and apply that commit to the source code at the server. For that also reason, pay attention with your .gitignore, as it might contain necessary files to run the server.

5. Run `eb create` to create the environment You can create the RDS during `eb create`. All of the options stay [here][eb_create]. Sample command:
    
    * {% highlight bash %}
      eb create testenv1 --database.engine mysql --database.username testusername --database.password testpassword --scale 1
      {% endhighlight %}

    * Again, remember to commit local repository before `eb create` or `eb deploy`.
    * If you set the database server this way, make sure you log in to that DB server to create a real production DB, either by ssh-ing into server, or directly from your IP address. If the DB server is MySQL, the command looks like: `mysql -h [database endpoint] -P [port] -u [username] -p`. Note that if you access the DB server directly from your own IP address, you should change that DB server's security group to allow incoming access from your IP address.
    * One more thing to note, if you are using EB and you choose Linux server. However, if your development environment is MacOS or Windows, then just `pip freeze` might not accurately reproduce your environment into server. In that case, be prepared to modify configuration file to add any missing dependencies. Example:

        - {% highlight yaml %}
          packages:
            yum:
              libxml2: []
              libxml2-devel: []
              libxslt: []
              libxslt-devel: []
          {% endhighlight %}

6. And this is pretty much is. If you have any error, check the log with `eb logs`. AWS EB also provides some very helpful commands below:
  
  * `eb printenv`: print the server environment variables
  * `eb console`: open the EB console in web browser
  * `eb open`: open your EB-hosted site in web browser
  * `eb ssh`: ssh into your server command line.
    - Your application is located here: `/opt/python/current/app`
    - If you want to run Python on that server, you should activate the environment by running these 2 commands:
      + `$ source /opt/python/run/venv/bin/activate`
      + `$ source /opt/python/current/env`
    - Your server wsgi configuration is located here: `/etc/httpd/conf.d/wsgi.conf`


If you decide *not* to create the database instance during `eb create`, you can basically follow this instruction ([Database RDS][python_eb_rds]):

1. [Create][rds_create] Amazon RDS DB instance
2. Log in to that instance, and create a production database
2. Establish database connection in the code (host, port, db name, username, password...)
3. Update the requirements.txt file (typically to include the database programming interface)
4. Deploy with EB


# Workflow:

1. Create new AWS RDS. During RDS creation, best practice is to create a new security group and assign that group to your database. That way, you can easily modify this specific RDS security's rule without affecting other components in your AWS
2. SSH into the newly created AWS RDS and create specific database (if you haven't during RDS instance creation), username and password for your Django application. After completing this step, we will have a working MySQL RDS that our Django application can use.

  - create user for mysql unix socket connection: `CREATE USER '[username]'@'localhost' IDENTIFIED BY '[password]';`
  - create user for tcp connection: `CREATE USER '[username]'@'%' IDENTIFIED BY '[password]';`
  - grant permission to user: `GRANT [permission type] ON [database].[table] TO '[user-name]'@'localhost';` or `GRANT [permission type] ON [database].[table] TO '[user-name]'@'%';`

3. Run `eb init`. This command will ask you several questions. The answers you give will be used by to create the application later.

4. Create `.ebextensions`, and check all the configurations:

[python_configuration]: http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-specific.html#command-options-python
[eb_environment_configuration]: http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customize-containers.html
[python_eb_rds]: http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-rds.html
[eb_create]: http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-create.html#eb3-createoptions
[rds_create]: http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_SettingUp.html

5. Test run with the production environment variables and settings to see if the site runs. If the site runs, then you can believe that it will run on server

6. Run `eb create [env_name]`

  - Error: `django.db.utils.OperationalError: (2003, "Can't connect to MySQL server on...` during `python manage.py migrate`
    + Look at RDS security group, open the RDS security group, edit inbound settings to include security group of elastic beanstalk. You can also follow the link [here](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.RDS.html#rds-external-defaultvpc) to connect external RDS to EB (I didn't).
  - Then I get this: `django.db.utils.OperationalError: (1366, "Incorrect string value:...` (probably Unicode problem). So I ssh into mysql, remove the old database, and create the new database with `CREATE DATABASE [name] CHARACTER SET utf8;`. I also revoke and regrant privileges to access that database to django user.
  - After fixing the above errors, deployment succeeds. However, upon navigating to the homepage, I get Bad Request (404). This problem probably arises due to the EB url is not registered with Django's ALLOWED_HOST, so I just add that URL to ALLOWED_HOSTS, and everything is fixed.

7. Use my own domain name to access the website. This process will require AWS Route 53 and will costs a little money a month (my estimation is at most ~$2) as Route 53 is not provided in Free-Tier. The process is simply documented [here](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customdomains.html). After setting up Route 53 and modifying DNS configuration, it takes about 10 minutes for those changes to take effect.

8. I sshed into the instance to create super user

9. I change debug mode to False. I also add substitute /media/ -> app/media/ inside Configuration > Software Configuration, and now the website also serves static and media files. Serving static files or not on the same server can be manually configured here `/etc/httpd/conf.d/wsgi.conf` with AWS EB, as superficially noted [here](https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/modwsgi/#serving-files)

  - Error: static files are served but media files are not. Ok because I actually typed in app/media instead of app/media/ (missing trailing slash)

10. Set up Solr

  - Modify EB security group to allow incoming TCP access from 127.0.0.1:8983 (Solr default address)