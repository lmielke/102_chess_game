# 102_chess_game
## This Notebook is for documentation only. You should not run the code directly. To use auto install, use readme_setup.py as specified below.

# 1. What am I

This is a simple django template with some pre implemented features such as:
- user signup, email confirmation,
- user logon, password create/change
- user authorization middleware
- blog style article/blog page to allow in tool documentation and commenting
- some param settings to allow multiple domains to map to this template (you may not need this, to remove, you have to make some changes the existing models and forms)
- some pre defined css sheet

To manually install in development, clone this repo and install the requirements.txt from the resources folder. Add my_stuff.py to the folder which contains settings.py
HINT: content of my_stuff.py can be seen blow under NOTES for 01_clone_repo. Lines 39-60

# 2. Development Setup and installation using the commands below (Windows only)

I use this installer because it meets my personal preferences. Use at own risk! Do not run this notebook directly but use readme_setup.py file instead. This will create a environment and install the requirements.txt.

If on Windows, use cmds below:
1. Clone repo into folder in which this repo will exist          --> (cd [venvs folder] && git clone https://github.com/lmielke/102_chess_game.git)
2. Copy the readme_setup.py file into your venvs folder        --> (cd 102_chess_game && copy readme_setup.py .. && cd ..)
3. Run readme_setup.py with arguments yourProjectName(repo will be renamed to) hostname(IP or localhost) --> (readme_setup.py 102_new_name http://localhost:8000)
    NOTE: The readme_setup.py is a nbconvert of readme_setup.jpynb. If necessary, it can be created by typing (jupyter nbconvert --to script readme_setup.ipynb) inside the repo folder.

# 2. Production setup on Ubuntu >= 16.04 & Apache

Follow the instructions in this youTube link: link is coming soon
NOTE: to install in Prod you have to make some changes to /resources/ubuntu_apache.sh


Resources: I use keepass to keep the install info in two seperate keepass entries
01_clone_repo
#################################################################################
    
Autotype Sequence: sudo apt update && sudo apt install git && cd /home{ENTER}{DELAY 30000}{URL}{ENTER}{DELAY 10000}sudo chown -R {USERNAME}:{USERNAME} /home{ENTER}{DELAY 1000}sudo chmod -R 777 /home{ENTER}nano {PASSWORD}{ENTER}{DELAY 1000}{NOTES}

    TITLE: 01_clone_repo
    USERNAME: myuser
    PASSWORD: /home/my_stuff.py
    URL: sudo git clone https://github.com/lmielke/102_chess_game.git

    NOTES:
        import socket

        # str here needs to be part of virtualenv in gcloud 
        PRODUCTION = 'prod' in socket.gethostname()
        print(f'HOSTNAME = {socket.gethostname()}')

        # only needed if reverse proxy is used
        PROXY_IPS = ['in-case-of.proxy']

        # gmail account for signup and pwd reset
        EMAIL_HOST = 'smtp.yourmail.com'
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True
        EMAIL_HOST_USER = 'yourMail@somewhere.com'
        EMAIL_HOST_PASSWORD = 'some§$"§%pass§$"word'

        # to debug in production set to True
        DEBUG_PROD = False

        # is added to allowed hosts
        PRODUCTION_IP = '35.123.<--'

Autotype generates the lines below: dont forget to change the params, to convirm you hit Ctrl+x, Y, ENTER

    sudo apt update && sudo apt install git && cd /home
    sudo git clone https://github.com/lmielke/102_chess_game.git
    sudo chown -R marvin:marvin /home
    sudo chmod -R 777 /home
    nano /home/my_stuff.py
    import socket

    # str here needs to be part of virtualenv in gcloud 
    PRODUCTION = 'prod' in socket.gethostname()
    print(f'HOSTNAME = {socket.gethostname()}')

    # is added to allowed hosts
    PRODUCTION_IP = '35.237.15.200'

    # only needed if reverse proxy is used
    PROXY_IPS = ['in-case-of.proxy']

    # gmail account for signup and pwd reset
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'blackpelican.rocks@gmail.com'
    EMAIL_HOST_PASSWORD = 'H;Y:c[$2o%;1G|qv'

    # to debug in production set to True
    DEBUG_PROD = False


02_install_project
#################################################################################

Autotype Sequence: cp /home/my_stuff.py {USERNAME}{ENTER}{DELAY 1000}cp {URL}/resources/{NOTES} /home/{NOTES}{ENTER}{DELAY 1000}chmod 777 /home/{NOTES}{ENTER}{DELAY 1000}./{NOTES}

    TITLE: 02_install_project
    USERNAME: /home/102_chess_game/web_project/web_project/my_stuff.py
    PASSWORD: empty
    URL: /home/102_chess_game
    NOTES: ubuntu_apache.sh

Autotype generates the lines below: to confirm, hit ENTER

    cp /home/my_stuff.py /home/102_chess_game/web_project/web_project/my_stuff.py
    cp /home/102_chess_game/resources/ubuntu_apache.sh /home/ubuntu_apache.sh
    chmod 777 /home/ubuntu_apache.sh
    ./ubuntu_apache.sh
