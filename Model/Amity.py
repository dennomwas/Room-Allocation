from Model.People import Staff, Fellow
from Model.Rooms import Office, LivingSpace
from random import choice


class Amity(object):

    def __init__(self):
        self.all_rooms = []
        self.all_persons = []

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

    def add_person(self, first_name, last_name, designation, accommodation_request='N'):
        """ Adds a person to the system and allocates the person to a random room"""

        # if first_name == '' or last_name == '':
        #     return "Name cannot be blank!"
        #
        # if designation not in ['staff', 'fellow']:
        #     return "Invalid Input! Designation can only be staff or fellow"
        #
        # if accommodation_request not in ['Y', 'y', 'N', 'n']:
        #     return "Invalid Input! Only Y/N allowed"

        # add staff
        if designation == 'staff':
            staff = Staff(first_name, last_name)

            # get random office
            available_rooms = [room for room in self.all_rooms if room.available_spaces > len(room.persons_allocatedt3)
                               and room.room_type == 'office']
            room_chosen = choice(available_rooms)
            staff.current_occupancy.append(room_chosen)
            self.all_persons.append(staff)
            # add staff to office
            room_chosen.persons_allocated.append(staff)

        else:
            fellow = Fellow(first_name, last_name,accommodation_request)

            # add fellow to all persons list
            self.all_persons.append(fellow)

            # get random office
            available_rooms = [room for room in self.all_rooms if room.available_spaces > 0
                               and room.room_type == 'office']
            room_chosen = choice(available_rooms)

            # add fellow to office
            room_chosen.persons_allocated.append(fellow)

            if accommodation_request in ["Y", "y"]:

                # get random livingspace
                available_rooms = [room for room in self.all_rooms if room.available_spaces > 0
                                   and room.room_type == 'livingspace']
                room_chosen = choice(available_rooms)

                # add fellow to livingspace
                room_chosen.fellows_allocated.append(fellow)


    def reallocate_person(self, identifier, room_name):
        """ Reallocate the person with  person_identifier  to  new_room_name """


    # reallocate a fellow (living space) - check in fellows_allocated []

    # reallocate a fellow (office space) = check in persons_allocated []
    # reallocate a staff (office space) = check in persons_allocated []

    def load_people(self, file_name):
        """ Adds people to rooms from a txt file """
        pass

    def print_allocations(self):
        # fellows_allocated + persons_allocated
        pass

    def print_unallocated(self):
        # unallocated persons = all_persons - (fellows_allocated + persons_allocated)
        pass

    def print_room(self):
        pass

    def save_state(self):
        pass

    def load_state(self):
        pass




dojo = Amity()
# dojo.create_room('livingspace', 'Oculus')
# dojo.create_room('office', 'valhalla')
# dojo.create_room('office', 'valhall')
dojo.create_room('office', 'valhal')
dojo.create_room('office', 'valhal')
dojo.create_room('livingspace', 'valha')
dojo.create_room('livingspace', 'valh')

#
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

dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')
# dojo.add_person('Dennis', 'Mwangi', 'staff' ,'y')



#dennis = Staff('Dennis','Mwangi')
# print(dennis.identifier)
#print(dojo.all_rooms)

print(dojo.all_persons)

print('all persons', len(dojo.all_persons))

print('All rooms', len(dojo.all_rooms))

print(dojo.all_rooms)
