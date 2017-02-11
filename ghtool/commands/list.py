import json

import datetime

from .base import Base
from ghtool.constants import BASE_GITHUB_ENDPOINT, DEFAULT_LIST_GITHUB_ENDPOINT, FIRST_BOUNDARY, SECOND_BOUNDARY
from ghtool.helpers import github_api


class List(Base):
    def run(self):
        options = self.options
        resp = []
        number_of_repositories = int(options['-n'])
        if options['<language>']:
            lang = options['<language>']
            today = datetime.date.today()
            today = datetime.datetime.strftime(today, "%Y-%m-%d")
            query = "created:{} language:{} ".format(today, lang)
            # sort = options['-s']
            # if sort not in List.available_sort_options():
            #     raise Exception("{} is not supported as sort option".format(sort))
            # order = options['-o']
            # if order not in List.available_order_options():
            #     raise Exception("{} is not supported as order option".format(order))
            repositories = []
            language_based_repositories = github_api(BASE_GITHUB_ENDPOINT + "/search" + DEFAULT_LIST_GITHUB_ENDPOINT,
                                                     params={"q": query})
            if language_based_repositories.status_code == 200:
                language_based_repositories = github_api(language_based_repositories.links.get("last").get("url"))
                if language_based_repositories.status_code == 200:
                    while True:
                        language_based_repositories = github_api(language_based_repositories.links.get("prev").get("url"))
                        if language_based_repositories.status_code == 200:
                            loaded_repositories = language_based_repositories.json()
                            repositories += loaded_repositories['items']
                            if language_based_repositories.links.get("prev") is None:
                                break
                        else:
                            if language_based_repositories.status_code == 403:
                                print "API rate limit problem. Sorting available results..."
                                break
                            else:
                                print "Request failed. Status code: {}\nMore info: {}".format(
                                    language_based_repositories.status_code, language_based_repositories.json().get('message'))
                                exit()
                else:
                    print "Request failed. Status code: {}\nMore info: {}".format(
                        language_based_repositories.status_code, language_based_repositories.json().get('message'))
                    exit()
            else:
                print "Request failed. Status code: {}\nMore info: {}".format(
                    language_based_repositories.status_code, language_based_repositories.json().get('message'))
                exit()

            repositories = sorted(repositories,
                                  key=lambda i: datetime.datetime.strptime(i['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                                  reverse=True)
            for rep in repositories[: number_of_repositories]:
                resp.append(rep)
            print(json.dumps({
                'total': len(repositories),
                'repositories': resp
            }))
        else:
            latest_repository_id = self.get_last_repository(FIRST_BOUNDARY, SECOND_BOUNDARY)
            repositories = []
            while True:
                if number_of_repositories < 100:
                    repositories = self.get_repositories(latest_repository_id, number_of_repositories)
                else:
                    repositories += self.get_repositories(latest_repository_id, number_of_repositories)

                if repositories is not None and len(repositories) >= number_of_repositories:
                    break
                latest_repository_id -= number_of_repositories
            repositories = sorted(repositories, key=lambda i: int(i['id']), reverse=True)
            for rep in repositories[:number_of_repositories]:
                resp.append(rep)
            print(json.dumps(resp))

    @classmethod
    def get_last_repository(cls, left, right):
        last_repo_id = (left + right) // 2
        params = {"since": last_repo_id}
        request_repositories = github_api(BASE_GITHUB_ENDPOINT + DEFAULT_LIST_GITHUB_ENDPOINT, params)
        if request_repositories.status_code == 200:
            repositories = request_repositories.json()
            if len(repositories) == 0:
                return cls.get_last_repository(left, last_repo_id)
            elif len(repositories) == 100:
                return cls.get_last_repository(last_repo_id, right)
            else:
                return repositories[len(repositories) - 1]['id']
        else:
            error = request_repositories.json()
            print("Request failed. Status code: {}\n More info: {}".format(request_repositories.status_code,
                                                                            error['message']))
            exit()

    @classmethod
    def get_repositories(cls, id, number_of_repos):
        params = {"since": id - number_of_repos}
        request_repositories = github_api(BASE_GITHUB_ENDPOINT + DEFAULT_LIST_GITHUB_ENDPOINT, params)
        if request_repositories.status_code == 200:
            return request_repositories.json()
        else:
            print "Request failed. Status code: {}\nMore info: {}".format(
                request_repositories.status_code, request_repositories.json().get('message'))
            exit()

    @staticmethod
    def available_sort_options():
        return ['starts', 'forks', 'updated']

    @staticmethod
    def available_order_options():
        return ['asc', 'desc']
