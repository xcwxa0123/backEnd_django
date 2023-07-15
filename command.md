创建依赖文件 pip freeze > requirements.txt
安装依赖文件 pip install -r requirements.txt
ps -ef | grep gunicorn 
pm2 start "nohup gunicorn --access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log --bind=0.0.0.0:8000 backEnd_django.wsgi &" --name=backend_py
gunicorn --bind=0.0.0.0:8000 backEnd_django.wsgi & 
pkill gunicorn

虚拟环境 source ~/project/back_end/backEnd_django/drfEnv/bin/activate
退出虚拟环境 deactivate


sudo systemctl start nginx

sudo systemctl reload nginx

sudo systemctl status nginx

sudo systemctl stop nginx

sudo systemctl enable nginx


sudo systemctl restart gunicorn.service

<!-- pm2 start ./index.mjs --name=nuxt_app
pm2 start ./index.mjs --name=nuxt_app --env production -->
pm2 start .output/server/index.mjs --name yuriservices2 --env production

pm2 start yuriservices.config.js --name yuriservices --env production

pm2 start chatmiddle/server/index.mjs --name chatmiddle --env production PORT=3021


sudo netstat -tupln

pm2 stop yuriservices
pm2 status

拉代码直接git pull 然后密码的地方输token

sudo nano /etc/profile
export MY_VAR="my value"
source /etc/profile
python -c 'import os; print(os.environ.get("BOOKS_APP_ENVIRONMENT"))'

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

xcwxa0123
XCWXa0123@#！

 sudo nano /etc/profile