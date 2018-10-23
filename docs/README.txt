this repo is meant to house the exploraiton and data science
artifacts from looking into https://www.pdc.wa.gov/browse/open-data

=================
Two data files in the main directory are static copies of PDC data sets (one is zipped since it exceeded the 25 MB file size limit for github)

The  python file currently includes all classes, functions, and a main section which loads the data and does some basic processing.


===========BEANSTALK SETUP=============
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html
=======================================

# Open virtual environment
%HOMEPATH%\eb-virt\Scripts\activate

# install Django
(eb-virt)~$ pip install django==2.1.1

# run the server
cd ebdjango
python manage.py runserver
ctrl-c


# Elastic Beanstalk setup
pip freeze > requirements.txt
mkdir .ebextensions
touch .ebextensions\django.config
vim django.config
paste in:
  option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: ebdjango/wsgi.py
    
# close virtualenv
deactivate


# Initialize your EB CLI repository named django-tutorial

eb init -p python-3.6 django-tutorial

# Access Key ID:
#   ********
# Secret Access Key:
#   ********

# set up some keys
eb init

# deploy
eb create django-env

eb status

vim settings.py 
  ALLOWED_HOSTS = ['eb-django-app-dev.elasticbeanstalk.com',
                   'django-env.mnk8qwmk69.us-west-2.elasticbeanstalk.com']
  
eb deploy

eb open
