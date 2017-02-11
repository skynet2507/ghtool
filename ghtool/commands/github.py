import os

import __root__
from ghtool.commands import Base


class Github(Base):
    def run(self):
        file_name = 'ghcredentials.txt'
        file_path = os.path.join(__root__.path(), file_name)
        # In purpose of testing
        if self.options['-t']:
            file_name = 'test.txt'
            file_path = os.path.join(__root__.path(),"tests", file_name)
        with open(file_path,"w") as file:
            file.write("Username: {}\n".format(self.options['<username>']))
            file.write("Password: {}".format(self.options['<password>']))
            file.close()
            print "Credentials saved."




