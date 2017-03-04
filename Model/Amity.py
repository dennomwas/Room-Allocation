from Model.People import Staff, Fellow
from Model.Rooms import Office, LivingSpace
import random


class Amity(object):
    all_rooms = []
    # living_spaces = []
    # offices = []

    all_persons = []
    # staff = []
    # fellows = []

    def create_room(self, room_name, room_type):

        if room_name not in self.all_rooms:
            if room_type == 'Living Space':
                room = LivingSpace(room_name)
                self.all_rooms.append(room)
            else:
                room = Office(room_name)
                self.all_rooms.append(room)
        else:
            return "Room already exist!"

        # if room exists
        #     give error
        # else:
        #     create room
        #     append room to all_rooms[]

    def add_person(self, first_name, last_name, accommodation_request='N'):

            # add new fellow
            new_person = Fellow(first_name, last_name, accommodation_request)

            # check if fellow already exists
            if new_person.identifier in self.all_persons:
                return new_person.first_name, "Already exists"

            # check if fellow wants accommodation
            if new_person.accommodation_request == 'Y':

                # check if room already exists
                for room in self.all_rooms:
                    if room.room_name not in self.all_rooms:
                        return room.room_name, " does not exist, please create the room first!"

                    # assign a fellow to a living space
                    if room.room_type == 'Living Space':
                        if room.max_capacity < 4:
                            room.fellows_allocated.append(new_person)
                            new_person.assigned_living_space = room.room_name
                            self.all_persons.append(new_person)
                        else:
                            return "Room is filled to capacity!"

            else:
                # add a staff
                new_person = Staff(first_name, last_name)

                # check if staff already exists
                if new_person.identifier in self.all_persons:
                    return "Person already exists"

                # check if room exists
                for room in self.all_rooms:
                    if room.room_name not in self.all_rooms:
                        return "Room does not exist, please create the room first!"

                # assign an office to staff
                if new_person.designation == 'Staff':
                    if room.max_capacity < 6:
                        room.staff_allocated.append(new_person)
                        new_person.assigned_office = room.room_name
                        self.all_persons.append(new_person)
                    else:
                        return "Room filled to capacity!"




        # check if room exists:
        #     give error "Room already exists"
        # check if person is fellow:
        #     add fellow
        #     append to fellow list
        #   check if fellow wants accommodation
        #       assign room randomly(for loop to check for available room and not occupied to max capacity)
        # check if person is staff:
        #     add staff
        #     append to staff list
        #   check if staff want office
        #        assign office randomly(for loop to check for available office and not occupied to max capacity)

    def reallocate_person(self):
        pass
    # check if person is allocated a room



    def load_people(self, file_name):
        pass

    def print_allocations(self):
        pass

    def print_unallocated(self):
        pass

    def print_room(self):
        pass

    def save_state(self):
        pass

    def load_state(self):
        pass









