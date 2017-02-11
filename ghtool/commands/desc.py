import base64
import json
import os
from os.path import abspath, dirname, join

import grequests

import __root__
from ghtool.constants import BASE_GITHUB_ENDPOINT
from ghtool.helpers import get_credentials
from .base import Base


class Desc(Base):

    def exception_handler(self, request, exception):
        print "Error during fetching url: {}".format(request.url)
        print exception
        print "\n"

    def run(self):
        repos_list = self.options.get('<repo>')
        if len(repos_list) == 0:
            this_dir = abspath(dirname(__file__))
            with open(join(this_dir, 'desc/desc.rst')) as file:
                long_description = file.read()
                print long_description
        else:
            base_url = BASE_GITHUB_ENDPOINT + '/repositories/'
            file_path = os.path.join(__root__.path(), 'ghcredentials.txt')
            username, password = get_credentials(file_path)
            requests = []
            for repo_id in repos_list:
                requests.append(grequests.get(base_url + repo_id, headers={
                    "Authorization": "Basic " + base64.urlsafe_b64encode("%s:%s" % (username, password))}))
            responses = grequests.map(requests, exception_handler=self.exception_handler)
            resp = []
            for r in responses:
                if r is not None and r.status_code == 200:
                    item = r.json()
                    resp.append({
                        "id": item['id'],
                        "name": item['name'],
                        "owner": item['owner']['login'],
                        "language": item['language'],
                        "stars": item['stargazers_count'],
                        "forks": item['forks'],
                        "description": item['description'],
                        "html": item['html_url']
                    })
                elif r.status_code == 403:
                    resp.append(r.json()['message'])
                elif r.status_code == 404:
                    resp.append("Repository not found")
            print json.dumps(resp)
