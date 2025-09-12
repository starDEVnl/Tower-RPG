import subprocess, sys, os
try:
    import requests
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
try:
    from cryptography.fernet import Fernet
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])

def version():
    print("Checking current version...")
    n_version = requests.get("https://raw.githubusercontent.com/starDEVnl/Tower-RPG/master/version.txt").text
    installed = False
    for x in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        if x == "version.txt":
            installed = True
    if installed:
        with open("version.txt", "r") as f:
            version = f.read()
    else:
        version = 0
    if not n_version == version:
        print("Installing files 1/3...")
        r = requests.get("https://raw.githubusercontent.com/starDEVnl/Tower-RPG/master/Encryption.py")
        with open("Encryption.py","w") as f:
            f.write(r.text)
        print("Installing files 2/3...")
        r = requests.get("https://raw.githubusercontent.com/starDEVnl/Tower-RPG/master/main_refresh.py")
        with open("main_refresh.py","w") as f:
            f.write(r.text)
        print("Installing files 3/3...")
        r = requests.get("https://raw.githubusercontent.com/starDEVnl/Tower-RPG/master/server.py")
        with open("server.py","w") as f:
            f.write(r.text)
        with open("version.txt", "w") as f:
            f.write(n_version)
        print("Installed all files!")
    else:
        print("Up to date!")
        
version()
