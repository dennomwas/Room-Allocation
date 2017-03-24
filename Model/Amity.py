import sqlite3
from random import choice
import pickle

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

        # get a list of all rooms
        all_rooms = self.all_rooms['office'] + self.all_rooms['livingspace']

        # check room exists
        check_name = [room.room_name for room in all_rooms if room.room_name == room_name]

        if check_name:
            return room_name + ' already exists!'

        room_mapping = {'livingspace': LivingSpace, 'office': Office}

        new_room = room_mapping[room_type](room_name)

        # add an office and a livingspace
        if room_type.lower() == "office":
            Amity.all_rooms['office'].append(new_room)

            return room_name + ' created Successfully!'
        else:
            Amity.all_rooms['livingspace'].append(new_room)

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
            Amity.all_persons.append(staff)

            # add staff to office
            self.allocate_office(staff)

        elif designation.lower() == 'fellow':
            fellow = Fellow(first_name, last_name, accommodation_request='N')
            print(first_name + ' added successfully!')

            # add fellow to all persons list
            Amity.all_persons.append(fellow)

            # add fellow to office
            self.allocate_office(fellow)

            if accommodation_request.lower() == 'y':

                # add fellow to livingspace
                self.allocate_living(fellow)

    def allocate_office(self, person):

        # office does not exist add to unallocated list
        if not Amity.all_rooms['office']:
            Amity.unallocated_office.append(person)
            return 'There is no office in the system!'

        # check for empty offices
        empty_offices = [all(office for office in Amity.all_rooms['office']
                             if len(office.persons_allocated) == office.max_capacity)]

        # no empty office add to unallocated list
        if not empty_offices:
            Amity.unallocated_office.append(person)
            return 'All offices are full!'

        # get a list of all offices
        all_offices = [office for office in Amity.all_rooms['office']
                       if len(office.persons_allocated) < office.max_capacity]

        # get a random office
        random_office = choice(all_offices)

        # add office to person
        person.current_occupancy = random_office

        # add person to office
        random_office.persons_allocated.append(person)

    def allocate_living(self, person):

            # living space does not exist add to unallocated list
            if not Amity.all_rooms['livingspace']:
                Amity.unallocated_livingspace.append(person)
                return 'The living space does not exist!'

            # check for empty living space
            empty_livingspace = [all(livingspace for livingspace in Amity.all_rooms['livingspace']
                                     if len(livingspace.persons_allocated) == livingspace.max_capacity)]

            # no empty living space add to unallocated list
            if not empty_livingspace:
                Amity.unallocated_livingspace.append(person)
                return 'All living spaces are full!'

            # get a list of all living spaces
            all_living = [livingspace for livingspace in Amity.all_rooms['livingspace']
                          if len(livingspace.persons_allocated) < livingspace.max_capacity]

            # get a random office
            random_living = choice(all_living)

            # add living spaces to person
            person.current_occupancy = random_living

            # add person to living spaces
            random_living.persons_allocated.append(person)

    def reallocate_person(self, identifier, room_name):
        """ Reallocate the person with  person_identifier  to  new_room_name """
        room_to_reallocate = None
        previous_room = None
        person_found = None

        # get a list of all rooms
        all_rooms = Amity.all_rooms['office'] + Amity.all_rooms['livingspace']

        # check for available rooms
        rooms_names = [room.room_name for room in all_rooms]

        if room_name not in rooms_names:
            return "Room not found!"

        # check person exists
        person_found = next((person for person in Amity.all_persons if person.identifier == int(identifier)), None)

        if not person_found:
            return "Person with id" + " " + str(identifier) + " not Found!"

        # pick room to reallocate
        room_to_reallocate = next((room for room in all_rooms if room.room_name == room_name), None)

        if not room_to_reallocate:
            return "Room to reallocate not Found!"

        # Check room still has space
        if len(room_to_reallocate.persons_allocated) == room_to_reallocate.max_capacity:
            return "Room is Filled to capacity!"

        # Check Staff cannot be allocated to a living Space
        if isinstance(person_found, Staff) and  isinstance(room_to_reallocate, LivingSpace):
            return "Allocating Staff to living space not Allowed!"

        # pick the previous room a person was in
        previous_room = person_found.current_occupancy
        print(previous_room)

        # check if person is moving to the same room type
        if previous_room == room_to_reallocate:
            return "Reallocations cannot be done to the same room!"

        # remove person from room he was in
        previous_room.persons_allocated.remove(person_found)

        # assign person to a new room
        room_to_reallocate.persons_allocated.append(person_found)
        return person_found.first_name + ' reallocated to ' + str(room_to_reallocate) + ' successfully!'

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
                return filename + ' successfully loaded to system...'

        except FileNotFoundError:
            return 'File not found, Please try again...'

        except Exception as e:
            return e

    def print_allocations(self, filename=None):
        """ Prints a list of allocations onto the screen """

        # get a list of all rooms
        all_rooms = self.all_rooms['office'] + self.all_rooms['livingspace']

        print('\n', 'OFFICES')
        for room in Amity.all_rooms['office']:
            print('\n', room.room_name)
            print('---------------------')
            if room.max_capacity > 0:
                print('\n'.join(str(person.identifier) + ' ' + person.first_name + ' ' + person.last_name
                                for person in room.persons_allocated))

        print('\n', 'LIVING SPACES')
        for room in Amity.all_rooms['livingspace']:
            print('\n', room.room_name)
            print('---------------------')
            if room.max_capacity > 0:

                print('\n'.join(str(person.identifier) + ' ' + person.first_name + ' ' + person.last_name
                                for person in room.persons_allocated))

        if filename:

            with open(filename, 'w') as export_file:
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
        print('\n'.join(str(person) for person in Amity.unallocated_office), '\n')

        print('UNALLOCATED TO LIVING SPACE')
        print('----------------------------')
        print('\n'.join(str(person) for person in Amity.unallocated_livingspace), '\n')

        if filename:
            try:
                with open(filename, 'w') as export_file:
                    for person in Amity.unallocated_office:
                        export_file.write('UNALLOCATED TO OFFICES \n')
                        export_file.write('-------------------------\n')
                        export_file.write('\n'.join(str(person.identifier) + ' ' + person.first_name + ' ' +
                                                    person.last_name
                                                    for person in Amity.unallocated_office) + '\n\n')
                        break

                    for person in Amity.unallocated_livingspace:
                        export_file.write('UNALLOCATED TO LIVING SPACES \n')
                        export_file.write('-------------------------------\n')
                        export_file.write('\n'.join(str(person) for person in Amity.unallocated_livingspace) + '\n\n')
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
        room = next((room for room in all_rooms if room.room_name == room_name), None)

        # check if room name exists
        if not room:
            return 'room name not found'

        room_details = room_name
        room_details += '-' *15 + '\n'

        room_details += '\n'.join(str(person) for person in room.persons_allocated)
        return room_details

    def save_state(self):

        db_connect = sqlite3.connect('amity_db')
        conn = db_connect.cursor()

        conn.execute("CREATE TABLE IF NOT EXISTS all_data "
                     "(dataID INTEGER PRIMARY KEY UNIQUE, "
                     "all_rooms TEXT, all_persons TEXT, unallocated_office TEXT, unallocated_livingspace TEXT)")

        all_rooms = pickle.dumps(Amity.all_rooms)
        all_persons = pickle.dumps(Amity.all_persons)
        unallocated_office = pickle.dumps(Amity.allocate_office)
        unallocated_livingspace = pickle.dumps(Amity.unallocated_livingspace)

        conn.execute("INSERT INTO all_data VALUES (null, ?, ?, ?, ?);",
                     (all_rooms, all_persons, unallocated_office, unallocated_livingspace))

        db_connect.commit()
        db_connect.close()

        return 'Data successfully exported to Database'

    def load_state(self):

        db_connect = sqlite3.connect('amity_db')
        conn = db_connect.cursor()
        conn.execute("SELECT * FROM all_data WHERE dataID = (SELECT MAX(dataID) FROM all_data)")
        data = conn.fetchone()

        Amity.all_rooms = pickle.loads(data[1])
        Amity.all_persons = pickle.loads(data[2])
        Amity.unallocated_office = pickle.loads(data[3])
        Amity.unallocated_livingspace = pickle.loads(data[4])


        return 'Successfully loaded data from the Database!'


dojo = Amity()
dojo.create_room('office','yellow')
dojo.create_room('office', 'white')
dojo.create_room('office', 'red')

dojo.create_room('livingspace', 'oculus')
dojo.create_room('livingspace', 'hog')
dojo.create_room('livingspace', 'narnia')


dojo.add_person('dennis','mwangi','fellow','y')
dojo.add_person('lio','githinji', 'fellow', 'y' )
dojo.add_person('mbarak', 'mbigo','staff')
dojo.add_person('jose','jere', 'staff')

# dojo.save_state()
dojo.load_state()
