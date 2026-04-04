创建依赖文件 pip freeze > requirements.txt
安装依赖文件 pip install -r requirements.txt
ps -ef | grep gunicorn 
pm2 start "nohup gunicorn --access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log --bind=0.0.0.0:8000 backEnd_django.wsgi &" --name=backend_py
gunicorn --bind=0.0.0.0:8000 backEnd_django.wsgi & 

gunicorn backEnd_django.wsgi:application --bind 0.0.0.0:8000

echo "alias pm2startback='pm2 start \"gunicorn backEnd_django.wsgi:application --bind 0.0.0.0:8000\" --name django'" >> ~/.bashrc
echo "alias pm2startfront='pm2 start pm2.config.cjs --name soymilk --env production'" >> ~/.bashrc
echo "alias soyenv='source /home/admin/SoySauce/backend/backEnd_django/soysauce/bin/activate'" >> ~/.bashrc
echo "alias cdbackendpro='cd /home/admin/SoySauce/backend/backEnd_django'" >> ~/.bashrc
echo "alias cdfrontendpro='cd /home/admin/SoySauce/frontend/soymilk'" >> ~/.bashrc
echo "alias see80='sudo lsof -i :80'" >> ~/.bashrc

source ~/.bashrc

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

 sudo nano /etc/profile