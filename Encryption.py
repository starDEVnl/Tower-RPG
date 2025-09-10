#Encryption
from cryptography.fernet import Fernet
import os
d_key = b'uUP2953kcwVQeiLFcZcQFDbC9FP61NPVh_biedSPiVM='


class Encryption():
    def __init__(self):
        dk = Fernet(d_key)
        save_dir = os.path.dirname(os.path.realpath(__file__))
        save_key = False
        for x in os.listdir(save_dir):
            if x == "save.txt":
                save_key = True
        if save_key:
            with open("save.txt", "rb") as f:
                data = f.read()
            l = data
            l = dk.decrypt(data)
            self.key = l
        else:
            self.key = Fernet.generate_key()
            l = self.key
            l = dk.encrypt(l)
            with open("save.txt", "wb") as f:
                f.write(l)
        self.f = Fernet(self.key)
    def encrypt(self, data):
        data = str(data)
        data = data.encode("utf-8")
        return self.f.encrypt(data).decode("utf-8")
    def decrypt(self, data):
        data = self.f.decrypt(data)
        return eval(data.decode("utf-8"))   
