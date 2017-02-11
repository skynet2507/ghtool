"""
ghtool

Usage:
  ghtool -h | --help
  ghtool --version
  ghtool list [<language>] [-n=<limit>] [-o=<order>] [-s=<sort>]
  ghtool desc [<repo>...]
  ghtool github <username> <password> [-t]
  ghtool test

Options:
  -h --help            Show this screen.
  --version            Show version.
  -n=<limit>           Number of repositories to return [default: 10]
  -o=<order>           Order languages [default: desc]
  -s=<sort>            Sort repositories. Available options are : stars, forks and updated [default: updated]
  -t                   Test

Examples:
  ghtool list                           Lists the number of the latest created Github public repos. Default value is 10.
  ghtool list -n                        Lists the N latest created Github public repos.
  ghtool list python                    Lists 10 latest created Github public repos written in Python.
                                        This is default number of repos
  ghtool list python -n                 Lists the N latest created Github public repos written in Python.
  ghtool desc                           Shows detailed options for desc command
  ghtool desc 1 2 3 4...<x>             Lists some details of the requested Github repos.
  ghtool github <username> <password>   Sets credentials for github access
  ghtool test                           Testing purpose

"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import ghtool.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items(): 
        if hasattr(ghtool.commands, k) and v:
            module = getattr(ghtool.commands, k)
            ghtool.commands = getmembers(module, isclass)
            command = [command[1] for command in ghtool.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
