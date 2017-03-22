import sqlite3
from random import choice

from Model.People import Staff, Fellow
from Model.Rooms import Office, LivingSpace


class Amity(object):

    all_rooms = {"office": [], "livingspace": []}
    all_persons = []
    unallocated_office = []
    unallocated_livingspace = []

    def create_room(self, room_type, room_name):
        """ Creates rooms in Amity """

        # check if string
        if not isinstance(room_type, str) and not isinstance(room_name, str):
            raise TypeError('room type and room name must be a string!')

        # check room exists
        all_rooms = self.all_rooms['office'] + self.all_rooms['livingspace']

        check_name = [room.room_name for room in all_rooms if room.room_name == room_name]

        if check_name:
            return room_name + ' already exists!'

        room_mapping = {'livingspace': LivingSpace, 'office': Office}

        new_room = room_mapping[room_type](room_name)

        # add an office and a livingspace
        if room_type.lower() == "office":
            self.all_rooms['office'].append(new_room)

            return room_name + ' created Successfully!'
        else:
            self.all_rooms['livingspace'].append(new_room)

            return room_name + ' created Successfully!'

    def add_person(self, first_name, last_name, designation, accommodation_request='N'):
        """ Adds a person to the system and allocates the person to a random room"""

        if not isinstance(first_name, str) and not isinstance(last_name, str):
            raise TypeError('First Name and Last Name cannot be a number!')

        # add staff
        if designation.lower() == 'staff':
            staff = Staff(first_name, last_name)
            print(first_name + ' added successfully! \n NB: Staff cannot be allocated a Living Space')

            # add staff to all persons list
            self.all_persons.append(staff)

            # add staff to office
            self.allocate_office(staff)

        elif designation.lower() == 'fellow':
            fellow = Fellow(first_name, last_name, accommodation_request='N')
            print(first_name + ' added successfully!')

            # add fellow to all persons list
            self.all_persons.append(fellow)

            # add fellow to office
            self.allocate_office(fellow)

            if accommodation_request.lower() == 'y':

                # add fellow to livingspace
                self.allocate_living(fellow)

    def allocate_office(self, person):

        # office does not exist add to unallocated list
        if not self.all_rooms['office']:
            self.unallocated_office.append(person)
            return 'There is no office in the system!'

        # check for empty offices
        empty_offices = [all(office for office in self.all_rooms['office']
                             if len(office.persons_allocated) == office.max_capacity)]

        # no empty office add to unallocated list
        if not empty_offices:
            self.unallocated_office.append(person)
            return 'All offices are full!'

        # get a list of all offices
        all_offices = [office for office in self.all_rooms['office']
                       if len(office.persons_allocated) < office.max_capacity]

        # get a random office
        random_office = choice(all_offices)

        # add office to person
        person.current_occupancy.append(random_office)

        # add person to office
        random_office.persons_allocated.append(person)

    def allocate_living(self, person):

            # living space does not exist add to unallocated list
            if not self.all_rooms['livingspace']:
                self.unallocated_livingspace.append(person)
                return 'The living space does not exist!'

            # check for empty living space
            empty_livingspace = [all(livingspace for livingspace in self.all_rooms['livingspace']
                                     if len(livingspace.persons_allocated) == livingspace.max_capacity)]

            # no empty living space add to unallocated list
            if not empty_livingspace:
                self.unallocated_livingspace.append(person)
                return 'All living spaces are full!'

            # get a list of all living spaces
            all_living = [livingspace for livingspace in self.all_rooms['livingspace']
                          if len(livingspace.persons_allocated) < livingspace.max_capacity]

            # get a random office
            random_living = choice(all_living)

            # add living spaces to person
            person.current_occupancy.append(random_living)

            # add person to living spaces
            random_living.persons_allocated.append(person)

    def reallocate_person(self, identifier, room_name):
        """ Reallocate the person with  person_identifier  to  new_room_name """
        room_to_reallocate = None
        previous_room = None
        person_found = None

        # check for available rooms
        all_rooms = self.all_rooms['office'] + self.all_rooms['livingspace']
        rooms_list = [room.room_name for room in all_rooms]

        if room_name not in rooms_list:
            return "Room not found!"

        # check person exists
        person_found = [person for person in self.all_persons if person.identifier == int(identifier)]

        if not person_found:
            return "Person with id" + " " + str(identifier) + " not Found!"

        # pick room to reallocate
        room_to_reallocate = [room for room in all_rooms if room.room_name == room_name]
        print(room_to_reallocate)

        if not room_to_reallocate:
            return "Room Not Found!"

        print(person_found)
        # Check room still has space
        if len(room_to_reallocate[0].persons_allocated) > room_to_reallocate[0].max_capacity:
            return "Room is Filled to capacity!"

        # Check Staff cannot be allocated to a living Space
        if isinstance(person_found[0], Staff) and room_to_reallocate[0].room_type == "livingspace":
            return "Allocating Staff to living space not Allowed!"

        # pick the previous room a person was in
        previous_room = person_found[0].current_occupancy

        # check if person is moving to the same room type
        if previous_room[0].room_name is room_to_reallocate[0].room_name:
            return "Reallocations can only be done to the same room Types!"

        # remove person from room he was in
        if previous_room:
            previous_room[0].persons_allocated.remove(person_found)

        # assign person to a new room
        room_to_reallocate[0].persons_allocated.append(person_found)

    def load_people(self, filename):
        """ Adds people to rooms from a txt file """

        # check if filename is a string
        if not isinstance(filename, str):
            raise TypeError("File name cannot be a number!")

        # get details from the text file
        try:
            with open(filename, 'r') as persons_file:
                persons = persons_file.readlines()

                for person in persons:
                    person_details = person.split()
                    first_name = person_details[0]
                    last_name = person_details[1]
                    designation = person_details[2]
                    accommodation = person_details[-1]

                    if accommodation.lower() == 'Y':
                        self.add_person(first_name, last_name, designation, accommodation)
                    else:
                        self.add_person(first_name, last_name, designation, accommodation)
                return filename + ' successfully loaded to system'

        except FileNotFoundError:
            return 'File not found, Please try again...'

        except Exception :
            return 'Something went wrong, Please try again!'

    def print_allocations(self, filename=None):
        """ Prints a list of allocations onto the screen """

        print('\n', 'OFFICES')
        for room in self.all_rooms['office']:
            print('\n', room.room_name)
            print('---------------------')
            if room.max_capacity > 0:
                print('\n'.join(str(person.identifier) + ' ' + person.first_name + ' ' + person.last_name
                                for person in room.persons_allocated))

        print('\n', 'LIVING SPACES')
        for room in self.all_rooms['livingspace']:
            print('\n', room.room_name)
            print('---------------------')
            if room.max_capacity > 0:

                print('\n'.join(str(person.identifier) + ' ' + person.first_name + ' ' + person.last_name
                                for person in room.persons_allocated))

        if filename:
            with open(filename, 'w') as export_file:
                all_rooms = self.all_rooms['office'] + self.all_rooms['livingspace']
                for room in all_rooms:
                    export_file.write(room.room_name + '\n')
                    export_file.write('---------------- \n')
                    if room.max_capacity > 0:
                        export_file.write('\n'.join(str(person.identifier) + ' ' +
                                                    person.first_name + ' ' + person.last_name
                                                    for person in room.persons_allocated)+'\n\n')
                return 'Successfully exported room allocations to ' + filename

    def print_unallocated(self, filename=None):
        """ Prints a list of unallocated people to the screen """

        print('UNALLOCATED TO OFFICES')
        print('------------------------')
        print('\n'.join(str(person) for person in self.unallocated_office), '\n')

        print('UNALLOCATED TO LIVING SPACE')
        print('----------------------------')
        print('\n'.join(str(person) for person in self.unallocated_livingspace), '\n')

        if filename:
            try:
                with open(filename, 'w') as export_file:
                    for person in self.unallocated_office:
                        export_file.write('UNALLOCATED TO OFFICES \n')
                        export_file.write('-------------------------\n')
                        export_file.write('\n'.join(str(person.identifier) + ' ' + person.first_name + ' ' +
                                                    person.last_name
                                                    for person in self.unallocated_office) + '\n\n')
                        break

                    for person in self.unallocated_livingspace:
                        export_file.write('UNALLOCATED TO LIVING SPACES \n')
                        export_file.write('-------------------------------\n')
                        export_file.write('\n'.join(str(person) for person in self.unallocated_livingspace) + '\n\n')
                        break
                    return 'Successfully exported unallocated people file to ' + filename

            except FileNotFoundError:
                return 'File not found, Please try again!'

            except Exception:
                return 'Something went wrong!'

    def print_room(self, room_name):
        """ Prints the names of all the people in the room_name  on the screen"""

        # get a list of all rooms
        all_rooms = self.all_rooms['office'] + self.all_rooms['livingspace']

        room = [room for room in all_rooms if room.room_name == room_name]

        # check if room name exists
        if not room:
            print('room name not found')
        else:
            print(room_name)
            print('-------------------\n')

            for person in room[0].persons_allocated:
                if not room[0].persons_allocated:
                    return 'Persons not available!'

                return str(person.identifier) + ' ' + person.first_name + ' ' + person.last_name

    def save_state(self):
        pass

        db_connect = sqlite3.connect('amity_db')
        connect = db_connect.cursor()

        # # create table in the database
        connect.execute("CREATE TABLE IF NOT EXISTS all_rooms"
                        "(id INTEGER PRIMARY KEY UNIQUE, room_name TEXT, room_type TEXT ) ")

        all_rooms = self.all_rooms['office'] + self.all_rooms['livingspace']
        get_rooms = [room.room_name for room in all_rooms]
        print(get_rooms)

        # connect.execute("INSERT INTO all_rooms VALUES (NULL, ? , ? );", get_rooms)

    def load_state(self):
        pass
