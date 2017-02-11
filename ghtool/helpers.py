""" Here goes all helpers functions. These functions are used in many method/classes so we keep them separately."""

import base64
import requests

from ghtool.commands.decorator import github_credentials
import os
import __root__


@github_credentials()
def github_api(query, params=None):
    file_path = os.path.join(__root__.path(), 'ghcredentials.txt')
    username, password = get_credentials(file_path)
    response = requests.get(query, params=params, headers={
        "Authorization": "Basic " + base64.urlsafe_b64encode("%s:%s" % (username, password))})
    return response


def get_credentials(path):
    username = None
    password = None
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            word = line.split(": ")
            if word[0] == "Username":
                username = word[1].split("\n")[0]
            elif word[0] == "Password":
                password = word[1]
        return username, password

