import unittest

from Model.Amity import Amity
from Model.People import Staff, Fellow
from Model.Rooms import Office, LivingSpace


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.facility = Amity()


    # def tearDown(self):
    #     self.facility = Amity()

    def test_create_room(self):

        # Assert no of rooms before a new one is added
        count1 = len(self.facility.all_rooms)
        self.assertEquals(len(self.facility.all_rooms), 2)

        live1 = LivingSpace('valhalla')
        self.assertIsInstance(live1.room_type, str, msg='room_type must be a string!')
        self.assertIsInstance(live1.room_name, str, msg='room name must be a string!')

        # Assert new room has been created
        self.facility.create_room('office', 'Ruby')
        self.assertEqual(len(self.facility.all_rooms), 2)

        # Assert room list has incremented
        count2 = len(self.facility.all_rooms)
        self.assertEqual(count1, count2)

        # Assert maximum office capacity
        office1 = Office('camelot')
        self.assertEqual(office1.max_capacity, 6)

        # Assert room created is an office
        self.assertEqual(office1.room_type, 'office')

        # Assert maximum living space capacity
        room1 = LivingSpace('dojo')
        self.assertEqual(room1.max_capacity, 4)

        # Assert room created is a living space
        self.assertEqual(room1.room_type, 'livingspace')

    def test_add_person(self):

        room = LivingSpace('oculus')
        new_staff = Staff('Dennis', 'Mwangi')
        room.persons_allocated.append(new_staff)
        new_staff.current_occupancy.append(room)

        self.assertIsInstance(new_staff.first_name, str, msg='First Name cannot be a number')
        self.assertIsInstance(new_staff.last_name, str, msg='Last Name cannot be a number!')

        self.assertIn(new_staff, room.persons_allocated, msg='person added to new room')
        self.assertIn(room, new_staff.current_occupancy, msg='room has a person')

        # Assert no of people before another person is added
        count1 = len(self.facility.all_persons)

        # Assert new person has been added
        self.facility.add_person('Dennis', 'Mwangi', 'Y')
        # self.assertEqual(len(Amity.fellows), 1)
        self.assertEqual(len(self.facility.all_persons), 1)

        # Assert all_persons list has been incremented
        count2 = len(self.facility.all_persons)
        self.assertNotEqual(count1, count2)

    def test_allocate_office(self):
        person = Staff('Dennis', 'Mwangi')
        room = Office('Narnia')

        self.assertNotIn(room, self.facility.all_rooms, msg='There is no office in the system!')
        self.assertNotEqual(len(room.persons_allocated), room.max_capacity, msg='Office not full!')

    def test_reallocate_person(self):

        # Assert fellow allocated to new room
        room = LivingSpace('oculus')
        new_staff = Staff('Dennis', 'Mwangi')
        room.persons_allocated.append(new_staff)
        new_staff.current_occupancy.append(room)

        self.assertIn(new_staff, room.persons_allocated, msg='person added to new room' )
        self.assertIn(room, new_staff.current_occupancy, msg='room has a person')

        # Assert room not found
        self.assertNotIn(room, self.facility.all_rooms, msg='Room not found')

        # assert person not found
        self.assertNotIn(new_staff, self.facility.all_persons, msg='person not found')

        # Assert fellow is allocated to a living space
        self.assertIn(new_staff, room.persons_allocated)

        # Assert print fellow allocated to a living space
        # self.assertEqual(new_fellow, room.fellows_allocated[0], msg="Fellow not assigned a living space")

        # remove fellow from living space
        room.persons_allocated.remove(new_staff)

        # reallocate fellow to office
        room2 = Office('Narnia')
        room2.persons_allocated.append(new_staff)

        # Assert fellow is not in living space
        self.assertNotIn(new_staff, room.persons_allocated, msg="person does not exist in Living space")

        # Assert fellow has been reallocated to an office
        self.assertIn(new_staff, room2.persons_allocated, msg="person added to Office")

    def test_load_people(self):
        pass

        # Amity.load_people('upload.txt')
        # self.assertEqual(len(Amity.all_persons), 7)
        # self.assertEqual(len(Amity.fellows), 4)
        # self.assertEqual(len(Amity.staff), 3)

    def test_save_state(self):
        pass


# if __name__ == '__main__':
#     unittest.main()





# ruby = LivingSpace("Ruby", "Living Space")
# ruby.fellows_allocated















