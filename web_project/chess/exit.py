import os, time
import subprocess

# to add to start menu in windowns
# add to C:\Users\Lars\AppData\Roaming\Microsoft\Windows\Start Menu
def exitGame(chPid):
    if chPid == os.getpid():
        print(f"\nclosing Game")
        subprocess.call(['Taskkill', '/PID', str(chPid), '/F'], shell=True)
        #subprocess.call(['Taskkill', '/IM', 'python.exe', '/F'], shell=True)
    else:
        print(f"Procsss: {os.getpid()} not closed, because got {chPid}")

if __name__ == '__main__':  
    exitGame('12345')