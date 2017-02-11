import os

import __root__

file_path = os.path.join(__root__.path(), 'ghcredentials.txt')


def github_credentials():
    def decor(handler):
        def check(self, *args, **kwargs):
            username = None
            password = None
            with open(file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    word = line.split(": ")
                    if word[0] == "Username":
                        username = word[1].split("\n")[0]
                    elif word[0] == "Password":
                        password = word[1]
            if username is None and password is None:
                print "No credentials.\nPlease run ghtool github <username> <password> set your credentials."
                exit()
            return handler(self, *args, **kwargs)
        return check
    return decor