#!/bin/bash
pipenv install currently not working

cd /home
mv 102_chess_game 102_chess_game
sudo apt -y update
sudo apt -y upgrade
sudo apt install -y python3-pip
sudo apt install build-essential libssl-dev libffi-dev python3-dev -y
sudo apt install apache2 -y
sudo apt install apache2-dev -y
python -m pip install --upgrade pip
pip3 install mod_wsgi
sudo apt install pipenv
cd /home/102_chess_game
pipenv install
pipenv install mod_wsgi
sudo chown -R marvin:marvin /home/102_chess_game
cd /home/102_chess_game/web_project
sudo mkdir /etc/wsgi-port-80
sudo chown -R marvin:marvin /etc/wsgi-port-80
sudo groupadd  www-data
sudo adduser  www-data  www-data
sudo chown -R :www-data /home/102_chess_game/web_project/media/
sudo chmod -R 775 /home/102_chess_game/web_project/media/
sudo chown -R :www-data /home/102_chess_game/web_project
sudo chmod 777 /home/102_chess_game/web_project
sudo chown :www-data /home/102_chess_game/web_project/102_chess_game.sqlite3
sudo chmod 664 /home/102_chess_game/web_project/102_chess_game.sqlite3
pipenv shell
python manage.py collectstatic
python manage.py runmodwsgi --server-root /etc/wsgi-port-80 --user www-data --group www-data --port 80 --url-alias /static static --url-alias /media media --setup-only
sudo apachectl stop
sudo /etc/wsgi-port-80/apachectl start
sudo cp /home/102_chess_game/conf_files/sshd_config /etc/ssh/sshd_config
sudo systemctl restart sshd
sudo apt install ufw -y
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow http/tcp
sudo ufw allow https/tcp
sudo ufw allow 3389
sudo ufw enable
sudo passwd marvin
netstat -nat | grep LISTEN
sudo ufw status
sudo /etc/wsgi-port-80/apachectl restart
sudo apt install xrdp
sudo apt remove lightdm
sudo apt install xfce4
sudo apt-get install xfce4-terminal tango-icon-theme
echo xfce4-session > ~/.xsession
sudo apt install libexo-1-0
sudo apt install firefox
sudo service xrdp restart
sudo /etc/wsgi-port-80/apachectl restart