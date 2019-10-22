# 102_chess_game (python 3.7) NOTE: install for python3.8 will fail
##To use auto install, use readme_setup.py as specified below.

# 1. What am I

This is a simple django template with some pre implemented features such as:
- online chess game which uses django rest framework and a simple jquery ajax call to update the board
- min/max player with tensorflow eval model (i used a simple sequential conv net to eval the board state)
- move player by drag/drop (currently not working on mobile because I dont use tuch events)
- user signup, email confirmation,
- user logon, password create/change
- user authorization middleware
- blog style article/blog page to allow in tool documentation and commenting
- some param settings to allow multiple domains to map to this template (you may not need this, to remove, you have to make some changes the existing models and forms)
- some pre defined css sheet

# 2. Installation
For manual development install, clone this repo and create the venv with requirements.txt from the resources folder. Add my_stuff.py to web_project >> web_project (same folder as settings.py).

HINT: The content of my_stuff.py can be seen below. 20 lines starting with: import socket


## 2.1. Development Setup and installation using the commands below (Windows only)

I use this installer because it meets my personal preferences! Use at own risk! Do not run the notebook directly but use readme_setup.py file instead. 
If on Windows, this will create and upgrade the environment and install the requirements.txt.

Using Windows shell, to auto install you can copy/paste the cmds below following "-->":
1. Create a folder for the credentials file my_stuff.py and add content (see below) current default dir is C:\python_venvs\99_snipp_block\dj_conf_files\my_stuff.py
2. Clone repo into folder in which this repo will exist        --> (cd [your_venvs_folder] && git clone https://github.com/lmielke/100_django_template.git)
3. Copy the readme_setup.py file into your venvs folder        --> (cd 100_django_template && copy readme_setup.py .. && cd ..)
4. Run readme_setup.py with the following arguments 
    yourProjectName hostname(IP or localhost)                  --> (readme_setup.py yourProjectName http://localhost:8000)

NOTE: The readme_setup.py is a nbconvert of readme_setup.jpynb. If necessary, it can be created by typing (jupyter nbconvert --to script readme_setup.ipynb) inside the repo folder.



# 2.2. Production setup on Ubuntu >= 16.04 & Apache in Google Cloud (steps might differ on other hosting platforms)

After creating your vm wait some minutes. Then open the vm shell and follow the instructions in this youTube link: link is coming soon

##01_clone_repo
#################################################################################


Run lines below in Ubuntu shell: change vm_user_name, change 777 to reasonable value after install

    sudo apt update && sudo apt install git && cd /home
    sudo git clone https://github.com/lmielke/102_chess_game.git
    sudo chown -R vm_user_name:vm_user_name /home
    sudo chmod -R 777 /home

This is my_stuff.py. change all relevant params: to convirm you hit Ctrl+x, Y, ENTER
    
    nano /home/my_stuff.py

    import socket

    # str here needs to be part of virtualenv in gcloud 
    PRODUCTION = 'prod' in socket.gethostname()
    print(f'HOSTNAME = {socket.gethostname()}')

    # only needed if reverse proxy is used
    PROXY_IPS = ['in-case-of.proxy']

    # mail account for signup and pwd reset
    EMAIL_HOST = 'smtp.yourmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'yourMail@somewhere.com'
    EMAIL_HOST_PASSWORD = 'some§$"§%pass§$"word'

    # to debug in production set to True
    DEBUG_PROD = False

    # is added to allowed hosts
    PRODUCTION_IP = '35.237.<--'


###Keepass Autotype Sequence of 01_clone_repo: 

sudo apt update && sudo apt install git && cd /home{ENTER}{DELAY 30000}{URL}{ENTER}{DELAY 10000}sudo chown -R {USERNAME}:{USERNAME} /home{ENTER}{DELAY 1000}sudo chmod -R 777 /home{ENTER}nano {PASSWORD}{ENTER}{DELAY 1000}{NOTES}

    TITLE: 01_clone_repo
    USERNAME: vm_user_name
    PASSWORD: /home/my_stuff.py
    URL: sudo git clone https://github.com/lmielke/102_chess_game.git

    NOTES:
        import socket

        # str here needs to be part of virtualenv in gcloud 
        PRODUCTION = 'prod' in socket.gethostname()
        print(f'HOSTNAME = {socket.gethostname()}')

        # only needed if reverse proxy is used
        PROXY_IPS = ['in-case-of.proxy']

        # mail account for signup and pwd reset
        EMAIL_HOST = 'smtp.yourmail.com'
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True
        EMAIL_HOST_USER = 'yourMail@somewhere.com'
        EMAIL_HOST_PASSWORD = 'some§$"§%pass§$"word'

        # to debug in production set to True
        DEBUG_PROD = False

        # is added to allowed hosts
        PRODUCTION_IP = '35.123.<--'


###Before installing you have to change the repo name inside line 3 of resources >> ubuntu_apache.sh
Change the to-value to what ever you like. Make sure, the name lines up with your 02_install_project names below.
Also, feel free to add/remove lines from ubuntu_apache.sh if needed.

    mv 102_chess_game yourProjectName


##02_install_project
#################################################################################

Run lines below in Ubuntu shell:
1. change 777 to reasonable value after install
2. You will be prompted to press Y/N several times. So, stay at your computer and confirm everything with yes.
3. You will be prompted for the remote desktop password. Enter a Password and convirm.
4. You will be asked to choose a desktop. I always go with the default (gdm3). Just press ENTER to confirm.

    cp /home/my_stuff.py /home/yourProjectName/web_project/web_project/my_stuff.py
    cp /home/yourProjectName/resources/ubuntu_apache.sh /home/ubuntu_apache.sh
    chmod 777 /home/ubuntu_apache.sh
    ./ubuntu_apache.sh


###Keepass Autotype Sequence for 02_install_project:

cp /home/my_stuff.py {USERNAME}{ENTER}{DELAY 1000}cp {URL}/resources/{NOTES} /home/{NOTES}{ENTER}{DELAY 1000}chmod 777 /home/{NOTES}{ENTER}{DELAY 1000}./{NOTES}

    TITLE: 02_install_project
    USERNAME: /home/yourProjectName/web_project/web_project/my_stuff.py
    PASSWORD: i keep my ssh key here
    URL: /home/yourProjectName
    NOTES: ubuntu_apache.sh


# 3. Template change
In admin there is a starting Theme/Article, that has a web_mode of localhost. This means, its only shown, if HOSTNAME is localhost:8000.
You can change web_mode to your hostname/IP to show Theme/Article in production.
You can directly access the game via url: yourDomainOrIp/chess/