#!/usr/bin/env python
# coding: utf-8

# # 102_chess_game
# ## This Notebook is for documentation only. You should not run the code directly. To use auto install, use readme_setup.py as specified below.

# # 1. What am I

# This is a simple django template with some pre implemented features such as:
# - user signup, email confirmation,
# - user logon, password create/change
# - user authorization middleware
# - blog style article/blog page to allow in tool documentation and commenting
# - some param settings to allow multiple domains to map to this template (you may not need this, to remove, you have to make some changes the existing models and forms)
# - some pre defined css sheet
# 
# To install in development, clone this repo and install the requirements.txt from the resources folder.

# # 2. Development Setup and installation using the code below (Windows only)

# I use this installer because it meets my personal preferences. Use at own risk! Do not run this notebook directly but use readme_setup.py file instead. This will create a environment and install the requirements.txt.
# 
# If on Windows, use cmds below:
# 1. Clone repo into folder in which this repo will exist          --> (cd [venvs folder] && git clone https://github.com/lmielke/102_chess_game.git)
# 2. Copy the readme_setup.py file into your venvs folder        --> (cd 102_chess_game && copy readme_setup.py .. && cd ..)
# 3. Run readme_setup.py with arguments yourProjectName(repo will be renamed to) hostname(IP or localhost) --> (readme_setup.py 102_new_name http://localhost:8000)
#     NOTE: The readme_setup.py is a nbconvert of this notebook. If necessary  it can be created by typing (jupyter nbconvert --to script readme_setup.ipynb) inside the repo folder.
# 4. Remove setup file --> (del/rm readme_setup.py)

# ## 2.1. here comes the code

# In[25]:


import multiprocessing, os, re, shutil, subprocess, sys, time
import argparse


# In[26]:


parser = argparse.ArgumentParser(description="wtf")
parser.add_argument('yourProjectName', help='Future Project-Name such as: 103_chess_game')
parser.add_argument('cloneProjectUrl', help='Clone url such as: https://github.com/lmielke/102_chess_game.git')

venvsPath = os.getcwd()
cloneProjectUrl = parser.parse_args().cloneProjectUrl
cloneProjectName = (os.path.basename(cloneProjectUrl)).split('.')[0]
yourProjectName = parser.parse_args().yourProjectName
print(f"your new project will be in: {venvsPath}/{yourProjectName}")
yourProjectPath = os.path.join(venvsPath, yourProjectName)
djProjectPath = os.path.join(yourProjectPath, "web_project")

def main(*args):
    # copies dj_setup.py from your local repository to django folder (its currently added to .gitignore do not upload this to a public repo)
    os.chdir(venvsPath)
    subprocess.call(["git", "clone", cloneProjectUrl], shell=True)
    myStuffPath = os.path.join(venvsPath, "99_snipp_block", "dj_conf_files", "my_stuff.py")
    existingEnvironments = os.listdir(venvsPath)
    if yourProjectName in existingEnvironments:
        print(f"AN Environement with name {yourProjectName} already exists in {venvsPath} \n{existingEnvironments}")
        print("you have 15 secs to abort by pressing Ctrl+C now")
        time.sleep(15)
    else:
        print("ready to go")
    # renames the template to what ever name you like
    if cloneProjectName != yourProjectName: os.rename(cloneProjectName, yourProjectName)
    os.chdir(os.path.join(yourProjectPath))
    # creates the envirionment inside yourProjectPath/venv folder
    subprocess.call(["pipenv", "install"], shell=True)
    try:
        print(myStuffPath)
        shutil.copyfile(myStuffPath, os.path.join(yourProjectPath, "web_project", "web_project", "my_stuff.py"))
    except:
        raise Exception("copying my_stuff.py failed because path does not exist! You have to manually adjust my_stuff.py. Its location is same as settings.py")
    os.chdir(os.path.join(yourProjectPath, "web_project"))
    subprocess.call(['pipenv', 'run', 'python', 'manage.py', 'makemigrations'], shell=True)
    subprocess.call(['pipenv', 'run', 'python', 'manage.py', 'migrate'], shell=True)
    return djProjectPath


# ### 2.1.2. Runs the django dev server (manage.py runserver) to test if its there

# In[28]:


def run_server(*args):
    os.chdir(djProjectPath)
    subprocess.call(['pipenv', 'run', 'python', 'manage.py', 'runserver'], shell=True)
    return True


# ### 2.1.3. Tests the django dev server and kills it after response check

# In[29]:


def test_server():
    import requests, time
    from datetime import datetime as dt
    from datetime import timedelta as td
    time.sleep(5)
    # CHPID is a comment in i_navbar_bottom.html template
    match = re.compile(r"(<CHPID>)(\d{3,6})(</CHPID>)")
    prcId = re.search(match, requests.get('http://localhost:8000').text)[2]
    subprocess.call(['TASKKILL', '/PID', str(prcId), '/F'], shell=True)
    if prcId:
        print(f"\n\n\tSUCCSESS: Server ran successfully with prcId: {prcId}\n\n")
    else:
        print(f"\n\n\tWARNING: Server run could not be confirmed\n\n")
    return True


# ### 2.1.4. This program is run in multiprocessing, in order to be able to run webserver and kill it after checking

# In[30]:


if __name__ == '__main__':
    if "django_template" in venvsPath:
        raise Exception("HANDLING ERROR: you can not run readme_setup.py from inside the django_template folder")
    prcId = None
    a = multiprocessing.Process(target=main, args=(cloneProjectName, yourProjectName, venvsPath, yourProjectPath, djProjectPath))
    b = multiprocessing.Process(target=run_server, args=(cloneProjectName, yourProjectName, venvsPath, yourProjectPath, djProjectPath))
    c = multiprocessing.Process(target=test_server)
    a.start()
    a.join()
    print("install is done")
    b.start()
    c.start()
    c.join()
    print(f"now deleting readme_setup.py from {os.getcwd()}")
    print("INSTALL COMPLETE")

