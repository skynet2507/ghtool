import json
from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestUserAuthentication(TestCase):
    def test_returns_fake_credentials(self):
        output = popen(['ghtool', 'github', 'aaa', 'bbb', '-t'], stdout=PIPE).communicate()[0]
        self.assertTrue("Credentials saved." in output)

    def test_10_latest_repos(self):
        output = popen(['ghtool', 'list'], stdout=PIPE).communicate()[0]
        result = json.loads(output)
        self.assertTrue(len(result) == 10)

    def test_last_30_repos(self):
        output = popen(['ghtool', 'list', '-n 30'], stdout=PIPE).communicate()[0]
        result = json.loads(output)
        self.assertTrue(len(result) == 30)

    def test_last_10_python_repos(self):
        output = popen(['ghtool', 'list', 'python'], stdout=PIPE).communicate()[0]
        try:
            result = json.loads(output)
            self.assertTrue(len(result['repositories']) == 10)
        except ValueError:
            print output
            self.assertTrue("API rate limit" in output)

    def test_first_item_python_repos(self):
        output = popen(['ghtool', 'list', 'python'], stdout=PIPE).communicate()[0]
        try:
            result = json.loads(output)
            self.assertTrue(result['repositories'][0]['language'], "Python")
        except ValueError:
            self.assertTrue("API rate limit" in output)

    def test_description(self):
        output = popen(['ghtool', 'desc'], stdout=PIPE).communicate()[0]
        self.assertTrue("DESCRIPTION" in output)

    def test_desc_repos(self):
        output = popen(['ghtool', 'desc', '81618459 1'], stdout=PIPE).communicate()[0]
        result = json.loads(output)
        self.assertTrue(len(result), 2)

        self.assertTrue(result[0]['id'], "81618459")
        self.assertTrue(result[0]['id'], "1")

    def test_repository_with_wrong_id(self):
        output = popen(['ghtool', 'desc', '2'], stdout=PIPE).communicate()[0]
        result = json.loads(output)
        self.assertTrue("Repository not found" in result[0])

    def test_new_command_without_run_function(self):
        output = popen(['ghtool', 'test'], stdout=PIPE).communicate()[0]
        print output
        try:
            # test.run()
            print "to"
        except NotImplementedError, message:
            print message
            self.assertTrue("run() method must be implemented", message)


