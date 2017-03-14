#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    Amity tcp <host> <port> [--timeout=<seconds>]
    Amity serial <port> [--baud=<n>] [--timeout=<seconds>]
    Amity (-i | --interactive)
    Amity (-h | --help | --version)
    Amity create_room <room_name> <room_type>...
    Amity add_person <first_name> <last_name> <FELLOW|STAFF> [<wants_accommodation>]
    reallocate_person <person_identifier> <new_room_name>
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --baud=<n>  Baudrate [default: 9600]
"""

import sys
import cmd
from Model.Amity import Amity
from docopt import docopt, DocoptExit


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):
    intro = 'Welcome to my interactive program!' \
        + ' (type help for a list of commands.)'
    prompt = '(Enter Command => ) '
    file = None
    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <OFFICE|LIVING SPACE> <room_name>..."""
        self.amity.create_room(arg['<room_type>'], arg['<room_name>'])

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <FELLOW|STAFF> [<wants_accommodation>]"""
        self.amity.add_person(arg['<first_name>'], arg['<last_name>'], arg['<designation>'])

    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name> """

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)