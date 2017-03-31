import pickle
import sqlite3
from os import remove
from os import path
from sqlite3 import Error
from random import choice

from Model.People import Staff, Fellow
from Model.Rooms import Office, LivingSpace


class Amity(object):

    all_rooms = {"office": [], "livingspace": []}
    all_persons = []
    unallocated_office = []
    unallocated_livingspace = []

    def create_room(self, room_type, room_name):

        """ Creates rooms in Amity
         get a list of all rooms
         check room exists
         create an office
         create a livingspace
        
        """
        all_rooms = self.all_rooms['office'] + self.all_rooms['livingspace']

        check_name = [room.room_name for room in all_rooms if room.room_name == room_name]

        if check_name:
            return room_name + ' already exists!'

        room_mapping = {'livingspace': LivingSpace, 'office': Office}

        new_room = room_mapping[room_type](room_name)

        if room_type.lower() == "office":
            Amity.all_rooms['office'].append(new_room)

            return room_name + ' created Successfully!'
        else:
            Amity.all_rooms['livingspace'].append(new_room)

            return room_name + ' created Successfully!'

    def add_person(self, first_name, last_name, designation, accommodation_request='N'):

        """ Adds a person to the system and allocates the person to a random room
        add staff
        add staff to all persons list
        add staff to office
        add fellow to all persons list
        add fellow to office
        add fellow to livingspace if accommodation request is yes
        
        """
        if designation.lower() == 'staff':
            staff = Staff(first_name, last_name)

            Amity.all_persons.append(staff)
            print(first_name + ' added successfully! \n NB: Staff cannot be allocated a Living Space')

            self.allocate_office(staff)

        elif designation.lower() == 'fellow':
            fellow = Fellow(first_name, last_name, accommodation_request='N')

            Amity.all_persons.append(fellow)
            print(first_name + ' added successfully!')

            self.allocate_office(fellow)

            if accommodation_request.lower() == 'y':

                self.allocate_livingspace(fellow)

    def allocate_office(self, person):

        """ This is a helper function to add person to office
        if there is no office in the system 
            add person to unallocated_office list
        check for empty office
        if none exist 
            return that all offices are full
            add person to unallocated_office list
        get a list of all offices
        get a random office
        make random office the persons current office
        add person to the persons_allocated list for the office
        
        """
        if not Amity.all_rooms['office']:
            Amity.unallocated_office.append(person)
            return 'There is no office in the system!'

        empty_offices = [all(office for office in Amity.all_rooms['office']
                             if len(office.persons_allocated) == office.max_capacity)]

        if not empty_offices:
            Amity.unallocated_office.append(person)
            return 'All offices are full!'

        all_offices = [office for office in Amity.all_rooms['office']
                       if len(office.persons_allocated) < office.max_capacity]

        random_office = choice(all_offices)

        person.current_office = random_office

        random_office.persons_allocated.append(person)

    def allocate_livingspace(self, person):

        """This is a helper function to add person to livingspaces
        if living space does not exist 
            add to unallocated list
            return livingspace does not exist
        check for empty living space
        if there's no empty living space 
            add to unallocated list
            return livingspace is full
        get a random livingspace
        make random the livingspace the persons current livingspace
        add person to the persons_allocated list for livingspace
        
        """
        if not Amity.all_rooms['livingspace']:
            Amity.unallocated_livingspace.append(person)
            return 'The living space does not exist!'

        empty_livingspace = [all(livingspace for livingspace in Amity.all_rooms['livingspace']
                                 if len(livingspace.persons_allocated) == livingspace.max_capacity)]

        if not empty_livingspace:
            Amity.unallocated_livingspace.append(person)
            return 'All living spaces are full!'

        all_living = [livingspace for livingspace in Amity.all_rooms['livingspace']
                      if len(livingspace.persons_allocated) < livingspace.max_capacity]

        random_living = choice(all_living)

        person.current_living = random_living

        random_living.persons_allocated.append(person)

    def reallocate_person(self, identifier, room_name):

        """ Reallocate the person with  person_identifier  to  new_room_name
         
        get a list of all rooms.
        check for available rooms.
        if there's no room assert room not found.
        check person exists.
        if not return person not found.
        pick room to reallocate.
        if not return room to reallocate not found.
        Check room still has space.
        if not return room is filled to capacity.
        Check Staff cannot be allocated to a living Space.
        if not return allocating space to livingspace not allowed.
        pick the previous room a person was in.
        check if person is moving to the same room type.
        if not return reallocations cannot be done to same room types.
        update the persons new office.
        update the persons new livingspace if fellow.
        check if person is fellow and currently in a livingspace.
        return fellow in livingspace cannot move to office.
        remove person from room he was in.
        assign person to a new room.
        if person in unallocated_office move to available office
        if person in unallocated_living move to available livingspace
        
        """
        room_to_reallocate = None
        previous_room = None
        person_found = None

        all_rooms = Amity.all_rooms['office'] + Amity.all_rooms['livingspace']

        rooms_names = [room.room_name for room in all_rooms]

        if room_name not in rooms_names:
            return "Room not found!"

        person_found = next((person for person in Amity.all_persons if person.identifier == int(identifier)), None)

        if not person_found:
            return "Person with id" + " " + str(identifier) + " not Found!"

        room_to_reallocate = next((room for room in all_rooms if room.room_name == room_name), None)

        if not room_to_reallocate:
            return "Room to reallocate not Found!"

        if len(room_to_reallocate.persons_allocated) == room_to_reallocate.max_capacity:
            return "Room is Filled to capacity!"

        if isinstance(person_found, Staff) and isinstance(room_to_reallocate, LivingSpace):
            return "Reallocating Staff to Living space not Allowed!"

        if isinstance(person_found, Fellow) and person_found.current_living:
            if room_to_reallocate.room_type == 'OFFICE':
                return "Reallocating Fellow in Living space to Office not Allowed!"

        if isinstance(room_to_reallocate, Office):
            previous_room = person_found.current_office
        else:
            previous_room = person_found.current_living

        if previous_room:

            if previous_room == room_to_reallocate:
                return "Reallocations cannot be done to the same room or Person is already in the room!"

            if isinstance(room_to_reallocate, Office):
                person_found.current_office = room_to_reallocate

            if isinstance(person_found, Fellow):
                person_found.current_living = room_to_reallocate

            previous_room.persons_allocated.remove(person_found)

            room_to_reallocate.persons_allocated.append(person_found)
            return person_found.first_name + ' reallocated to ' + str(room_to_reallocate) + ' successfully!'

        if person_found in Amity.unallocated_office and isinstance(room_to_reallocate, Office):

            room_to_reallocate.persons_allocated.append(person_found)

            Amity.unallocated_office.remove(person_found)
            return person_found.first_name + ' allocated to ' + str(room_to_reallocate) + ' successfully!'

        if person_found in Amity.unallocated_livingspace and isinstance(room_to_reallocate, LivingSpace):

            room_to_reallocate.persons_allocated.append(person_found)

            Amity.unallocated_livingspace.remove(person_found)
            return person_found.first_name + '  allocated to ' + str(room_to_reallocate) + ' successfully!'

    def load_people(self, filename):

        """ Adds people to rooms from a txt file 
        check if filename is a string
        get details from the text file
        
        """
        if not isinstance(filename, str):
            return "Please check your file name and try again!"

        try:
            with open(filename, 'r') as persons_file:
                persons = persons_file.readlines()

                for person in persons:
                    person_details = person.split()
                    first_name = person_details[0]
                    last_name = person_details[1]
                    designation = person_details[2]
                    accommodation = person_details[-1]

                    if accommodation.lower() == 'y':
                        self.add_person(first_name, last_name, designation, accommodation)
                    else:
                        self.add_person(first_name, last_name, designation, accommodation)
                return filename + ' successfully loaded to system...'

        except FileNotFoundError:
            return 'File not found, Please try again...'

        except Exception as e:
            return e

    def print_allocations(self, filename=None):

        """ Prints a list of allocations onto the screen 
        get a list of all rooms
        display allocated offices
        display allocated livingspaces
        export allocations to a text file
        
        """
        all_rooms = self.all_rooms['office'] + self.all_rooms['livingspace']

        print('\n', 'OFFICES')
        for room in Amity.all_rooms['office']:
            print('\n', room.room_name)
            print('---------------------')
            if room.max_capacity > 0:
                print('\n'.join(str(person.identifier) + ', ' + person.first_name + ', '
                                + person.last_name + ', ' + person.person_type
                                for person in room.persons_allocated))

        print('\n', 'LIVING SPACES')
        for room in Amity.all_rooms['livingspace']:
            print('\n', room.room_name)
            print('---------------------')
            if room.max_capacity > 0:

                print('\n'.join(str(person.identifier) + ', ' + person.first_name + ', '
                                + person.last_name + ', ' + person.person_type
                                for person in room.persons_allocated))

        if filename:

            path = './files/'
            with open(path + filename, 'w') as export_file:
                for room in all_rooms:
                    export_file.write(room.room_name + '\n')
                    export_file.write('---------------- \n')
                    if room.max_capacity > 0:
                        export_file.write('\n'.join(str(person.identifier) + ', ' +
                                                    person.first_name + ', ' + person.last_name
                                                    for person in room.persons_allocated)+'\n\n')
                return 'Successfully exported room allocations to ' + filename

    def print_unallocated(self, filename=None):

        """ Prints a list of unallocated people to the screen 
        display unallocated offices
        display unallocated livingspaces
        export all to a text file
        
        """
        print('\n UNALLOCATED TO OFFICES')
        print('------------------------')
        print('\n'.join(str(person) for person in Amity.unallocated_office), '\n')

        print('\n UNALLOCATED TO LIVING SPACE')
        print('----------------------------')
        print('\n'.join(str(person) for person in Amity.unallocated_livingspace), '\n')

        if filename:
            try:
                path = './files/'
                with open(path + filename, 'w') as export_file:
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

        """ Prints the names of all the people in the room_name  on the screen
        get a list of all rooms
        check if room name exists
        print the room details
        
        """
        all_rooms = self.all_rooms['office'] + self.all_rooms['livingspace']
        room = next((room for room in all_rooms if room.room_name == room_name), None)

        if not room:
            return 'room name not found'

        print('\n', room_name)
        print('--------------------------')

        print('\n'.join(str(person) for person in room.persons_allocated) + '\n\n')

    def save_state(self, db_file):

        """ Persists all the data stored in the app to an SQLite database
        set the directory path
        connect to the database
        create a table if none exists and push the data to it
        save all the data into the database
        close the database connection

        """

        path = './database/'
        db_connect = sqlite3.connect(path + db_file)
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

    def load_state(self, db_file):

        """ Loads data from a database into the application
        set the directory path
        connect to the database
        select all data from the database table
        load the data into the application
        close the database connection
        
        """
        try:
            path = './database/'
            db_connect = sqlite3.connect(path + db_file)
            conn = db_connect.cursor()

            conn.execute("SELECT * FROM all_data WHERE dataID = (SELECT MAX(dataID) FROM all_data)")
            data = conn.fetchone()

            Amity.all_rooms = pickle.loads(data[1])
            Amity.all_persons = pickle.loads(data[2])
            Amity.unallocated_office = pickle.loads(data[3])
            Amity.unallocated_livingspace = pickle.loads(data[4])

            db_connect.close()
            return 'Successfully loaded data from the Database!'

        except Error:
            remove(path + db_file)
            return "Database not found, Please check the name and try again!"