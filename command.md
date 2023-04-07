pip freeze > requirements.txt
ps -ef | grep gunicorn
gunicorn --bind=0.0.0.0:8000 backEnd_django.wsgi &
source djangoEnv/bin/activate
deactivate


sudo systemctl start nginx

sudo systemctl reload nginx

sudo systemctl status nginx

sudo systemctl stop nginx

sudo systemctl enable nginx