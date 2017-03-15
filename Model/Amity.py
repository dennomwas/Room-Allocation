from Model.People import Staff, Fellow
from Model.Rooms import Office, LivingSpace
from random import choice


class Amity(object):
    all_rooms = []
    all_persons = []
    #
    # def __init__(self):
    #     self.all_rooms = []
    #     self.all_persons = []

    def create_room(self, room_type, room_name):
        """ Creates rooms in Amity """

        # check if string
        if not isinstance(room_type, str):
            raise TypeError('room_type must be a string!')

        if not isinstance(room_name, str):
            raise TypeError('room_name must be a string!')

        # check room exists
        all_rooms = [room.room_name for room in self.all_rooms]
        if room_name in all_rooms:
            return 'Room already exists!'

        if room_name.lower() not in ('livingspace', 'office'):

            room_mapping = {'livingspace': LivingSpace, 'office': Office}

            new_room = room_mapping[room_type](room_name)
            self.all_rooms.append(new_room)

    def add_person(self, first_name, last_name, designation, accommodation_request=None):
        """ Adds a person to the system and allocates the person to a random room"""

        # if first_name == '' or last_name == '':
        #     return "Name cannot be blank!"
        #
        # if designation not in ['staff', 'fellow']:
        #     return "Invalid Input! Designation can only be staff or fellow"
        #
        # if accommodation_request not in ['Y', 'y', 'N', 'n']:
        #     return "Invalid Input! Only Y/N allowed"
        if not isinstance(first_name, str):
            raise TypeError('First Name cannot be a number!')

        if not isinstance(last_name, str):
            raise TypeError('Last Name cannot be a number!')

        # add staff
        if designation == 'staff':
            staff = Staff(first_name, last_name)

            # add staff to all persons list
            self.all_persons.append(staff)

            # pick an office from all rooms list
            for room in self.all_rooms:
                if len(room.persons_allocated) < room.max_capacity and room.room_type == 'office':

                    # add office to staff
                    staff.current_occupancy.append(room)

                    # add staff to office
                    room.persons_allocated.append(staff)
                    break
                else:
                    print('full')
                    return "Room not available or is full!"

        else:
            fellow = Fellow(first_name, last_name, accommodation_request=None)

            # add fellow to all persons list
            self.all_persons.append(fellow)

            # pick an office from all rooms list
            for room in self.all_rooms:
                if len(room.persons_allocated) < room.max_capacity and room.room_type == 'office':

                    # add office to staff
                    fellow.current_occupancy.append(room)

                    # add fellow to office
                    room.persons_allocated.append(fellow)
                    break
                else:
                    return "Room not available or is full!"

            if accommodation_request == 'y':

                # pick a livingspace from all rooms list
                for room in self.all_rooms:
                    if len(room.persons_allocated) < room.max_capacity and room.room_type == 'livingspace':

                        # add livingspace to fellow
                        fellow.current_occupancy.append(room)

                        # add fellow to livingspace
                        room.persons_allocated.append(fellow)
                        break
                    else:
                        return "Room not available or is full!"

    def reallocate_person(self, identifier, room_name):
        """ Reallocate the person with  person_identifier  to  new_room_name """

    def load_people(self, filename):
        """ Adds people to rooms from a txt file """

        # check if file is blank
        if filename == '':
            print("File name cannot be blank")

        # check if filename is a string
        if not isinstance(filename, str):
            raise TypeError("File name cannot be a number!")

        # get details from the text file
        try:
            for person in open(filename):
                person = person.strip()
                person_details = person.split()
                first_name = person_details[0]
                last_name = person_details[1]
                designation = person_details[2]

                # add people found to rooms
                if len(person) == 4:
                    accommodation = person_details[3]
                else:
                    accommodation = None
                self.add_person(first_name, last_name, designation, accommodation)

        except FileNotFoundError as e:
            print(e)

        except Exception:
            print("Something went wrong, please try again!")

    def print_allocations(self, room_name):
        """ Prints a list of allocations onto the screen """
        # fellows_allocated + persons_allocated
        #for person in self.all_persons:
        print('\n'.join(str(person) for person in self.all_persons))

    # print
    # '\n'.join(str(p) for p in myList)

    def print_unallocated(self):
        """ Prints a list of unallocated people to the screen """

        # unallocated persons = all_persons - office(persons_allocated) + living(persons_allocated


    def print_room(self, room_name):
        """ Prints the names of all the people in the room_name  on the screen"""

        # if not isinstance(room_name, str):
        #     raise TypeError("Room name cannot be a number!")

        # get list of rooms to check if room name exists
        room_to_print = [room.room_name for room in self.all_rooms]

        # print people found in the room
        if room_name in room_to_print:
            print(room_name)
            print('-----------------------------------')
            print(room_name.persons_allocated)






        else:
            return "Room not found!"





    def save_state(self):
        pass

    def load_state(self):
        pass




dojo = Amity()
# dojo.create_room('livingspace', 'Oculus')
# dojo.create_room('office', 'valhalla')
dojo.create_room('office', 'valhalla')
dojo.create_room('office', 'krypton')
dojo.create_room('office', 'kampala')
dojo.create_room('livingspace', 'oculus')
dojo.create_room('livingspace', 'narnia')


# dojo.add_person('Dennis', 'Mwangi', 'fello' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'fellw' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'sta' ,'y')
# dojo.add_person('Dennis', 'Mwangi1', 'fellow' ,'n')
# dojo.add_person('Dennis', 'Mwangi2', 'fellow' ,'y')
# dojo.add_person('Dennis', 'Mwangi3', 'fellow' ,'n')
# dojo.add_person('Dennis', 'Mwangi4', 'fellow' ,'y')
# dojo.add_person('Dennis', 'Mwangi5', 'fellow' ,'y')
# dojo.add_person('Dennis', 'Mwangi6', 'fellow' ,'y')
# dojo.add_person('Dennis', 'Mwangi7', 'fellow' ,'y')
# dojo.add_person('Dennis', 'Mwangi8', 'fellow' ,'y')
# dojo.add_person('Dennis', 'Mwangi9', 'fellow' ,'y')
#
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')


#dojo.reallocate_person(4435144600,'valhalla')

dojo.load_people('upload.txt')

# dojo.print_room('valhalla')

dojo.print_allocations('valhalla')
#dennis = Staff('Dennis','Mwangi')
# print(dennis.identifier)
#print(dojo.all_rooms)
#
# print(dojo.all_persons)
#
# print('all persons', len(dojo.all_persons))
#
# print('All rooms', len(dojo.all_rooms))
#
# print(dojo.all_rooms)
