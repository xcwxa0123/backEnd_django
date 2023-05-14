创建依赖文件 pip freeze > requirements.txt
安装依赖文件 pip install -r requirements.txt
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
pm2 status

拉代码直接git pull 然后密码的地方输token

sudo nano /etc/profile
export MY_VAR="my value"
source /etc/profile
python -c 'import os; print(os.environ.get("BOOKS_APP_ENVIRONMENT"))'

python manage.py makemigrations
python manage.py migrate