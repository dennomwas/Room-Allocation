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
        count1 = len(Amity.all_rooms)
        self.assertEquals(len(Amity.all_rooms), 0)

        # Assert new room has been created
        self.facility.create_room('Ruby', 'living_spaces')
        self.assertEqual(len(Amity.all_rooms), 1)
        self.assertEqual(len(Amity.living_spaces), 1)

        # Assert room list has incremented
        count2 = len(Amity.all_rooms)
        self.assertNotEqual(count1, count2)

        # Assert maximum office capacity
        office1 = Office('camelot', 'office')
        self.assertEqual(office1.max_capacity, 6)

        # Assert room created is an office
        self.assertEqual(office1.room_type, 'office')

        # Assert maximum living space capacity
        room1 = LivingSpace('dojo', 'living space')
        self.assertEqual(room1.max_capacity, 4)

        # Assert room created is a living space
        self.assertEqual(room1.room_type, 'living space')

    def test_add_person(self):

        # Assert no of people before another person is added
        count1 = len(Amity.all_persons)

        # Assert new person has been added
        self.facility.add_person('Dennis', 'Mwangi', 'Y')
        self.assertEqual(len(Amity.fellows), 1)
        self.assertEqual(len(Amity.all_persons), 1)

        # Assert all_persons list has been incremented
        count2 = len(Amity.all_persons)
        self.assertNotEqual(count1, count2)

    def test_reallocate_person(self):

        # Assert fellow allocated to new room
        room = LivingSpace('oculus', 'living space')
        new_fellow = Fellow('Dennis', 'Mwangi', 'Y')
        room.fellows_allocated.append(new_fellow)

        # Assert fellow is allocated to a living space
        self.assertIn(new_fellow, room.fellows_allocated)

        # Assert print fellow allocated to a living space
        # self.assertEqual(new_fellow, room.fellows_allocated[0], msg="Fellow not assigned a living space")

        # remove fellow from living space
        room.fellows_allocated.remove(new_fellow)

        # reallocate fellow to office
        room2 = Office('Narnia', 'Office')
        room2.persons_allocated.append(new_fellow)

        # Assert fellow is not in living space
        self.assertNotIn(new_fellow, room.fellows_allocated, msg="person does not exist in Living space")

        # Assert fellow has been reallocated to an office
        self.assertIn(new_fellow, room2.persons_allocated, msg="person added to Office")

    def test_load_people(self):

        Amity.load_people('upload.txt')
        self.assertEqual(len(Amity.all_persons), 7)
        self.assertEqual(len(Amity.fellows), 4)
        self.assertEqual(len(Amity.staff), 3)

    def test_save_state(self):
        pass


# if __name__ == '__main__':
#     unittest.main()





# ruby = LivingSpace("Ruby", "Living Space")
# ruby.fellows_allocated















