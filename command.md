pip freeze > requirements.txt
ps -ef | grep gunicorn
gunicorn --bind=0.0.0.0:8000 backEnd_django.wsgi &
虚拟环境 source djangoEnv/bin/activate
退出虚拟环境 deactivate


sudo systemctl start nginx

sudo systemctl reload nginx

sudo systemctl status nginx

sudo systemctl stop nginx

sudo systemctl enable nginx


sudo systemctl restart gunicorn.service

pm2 start ./index.mjs --name=nuxt_app