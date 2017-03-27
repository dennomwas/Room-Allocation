#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    Amity tcp <host> <port> [--timeout=<seconds>]
    Amity serial <port> [--baud=<n>] [--timeout=<seconds>]
    Amity (-i | --interactive)
    Amity (-h | --help | --version)
    Amity create_room ( office|livingspace ) <room_name>...
    Amity add_person <first_name> <last_name> (fellow|staff) [<wants_accommodation>]
    Amity reallocate_person <person_identifier> <room_name>
    Amity load_people [<filename>]
    Amity print_allocations [-o=filename]
    Amity print_allocations [-o=filename]
    Amity save_state [--db=sqlite_database]

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --baud=<n>  Baudrate [default: 9600]
"""

import sys
import cmd
from termcolor import colored

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
    print('******************************************')
    intro = 'AMITY ROOM ALLOCATION SYSTEM! \n\n' + colored('[type help for a list of commands!]', 'yellow')
    print('******************************************')

    prompt = colored('Enter Command => ', 'red')

    # file = None
    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room (office|livingspace) <room_name>..."""

        room_type = 'office' if arg['office'] else 'livingspace'
        room_names = arg['<room_name>']
        for room_name in room_names:
            print(self.amity.create_room(room_type, room_name))

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> (fellow|staff) [<wants_accommodation>]"""

        designation = 'fellow'if arg['fellow'] else 'staff'
        accommodation = arg['<wants_accommodation>'] or 'N'

        self.amity.add_person(arg['<first_name>'],
                              arg['<last_name>'], designation, accommodation)

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <room_name> """

        print(self.amity.reallocate_person(arg['<person_identifier>'], arg['<room_name>']))

    @docopt_cmd
    def do_load_people(self, arg):
        """ Usage: load_people [<filename>]"""
        print(self.amity.load_people(arg['<filename>']))

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]  """

        print(self.amity.print_allocations(arg['--o']))

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_allocations [--o=filename]  """

        print(self.amity.print_unallocated(arg['--o']))

    @docopt_cmd
    def do_print_room(self, arg):
        """ Usage: print_room <room_name>  """

        print(self.amity.print_room(arg['<room_name>']))

    @docopt_cmd
    def do_save_state(self, arg):
        """ Usage save_state [--db=sqlite_database] """

    @docopt_cmd
    def do_load_state(self, arg):
        """ Usage load_state <sqlite_database> """

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)