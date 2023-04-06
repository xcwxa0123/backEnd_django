pip freeze > requirements.txt
ps -ef | grep gunicorn
gunicorn --bind=0.0.0.0:8000 backEnd_django.wsgi &