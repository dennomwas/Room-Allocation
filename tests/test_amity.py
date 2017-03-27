import unittest

from Model.Amity import Amity
from Model.People import Staff, Fellow
from Model.Rooms import Office, LivingSpace


class TestAmity(unittest.TestCase):
    def setUp(self):
        self.facility = Amity()
        self.facility.create_room('office', 'tsavo')
        self.facility.create_room('livingspace', 'home')

        self.facility.add_person('dennis', 'mwangi', 'fellow', 'y')
        self.facility.add_person('john', 'doe', 'staff', 'y')


    def test_create_room(self):

        self.assertEqual('tsavo already exists!',
                         self.facility.create_room('office', 'tsavo'))

        self.assertEqual('home already exists!',
                         self.facility.create_room('livingspace', 'home'))

    def test_no_office_in_the_system(self):
        self.assertNotEqual('There is no office in the system!',
                            self.facility.allocate_office(Fellow))

    def test_no_livingspace_in_the_system(self):
        self.assertNotEqual('The living space does not exist!',
                            self.facility.allocate_living(Staff))

    def test_offices_are_full(self):
        self.assertNotEqual('All offices are full!',
                            self.facility.allocate_living(Staff))

    def test_file_not_loaded(self):
        self.assertEqual('File not found, Please try again...',
                         self.facility.load_people('files/not_loaded.txt'))

    def test_file_loaded_successfully(self):
        self.assertEqual('upload.txt successfully loaded to system...',
                         self.facility.load_people('upload.txt'))

    def test_unallocated_not_exported(self):
        self.assertEqual('File not found, Please try again!',
                         self.facility.print_unallocated('files/name'))

    def test_unallocated_exported(self):
        self.assertEqual('Successfully exported unallocated people file to unallocated.txt',
                         self.facility.print_unallocated('unallocated.txt'))

    def test_file_exported(self):
        self.assertEqual('Successfully exported room allocations to export.txt',
                         self.facility.print_allocations('export.txt'))

    def test_print_room(self):
        self.assertEqual('room name not found',
                         self.facility.print_room('dojo'))

    def test_livingspace_does_not_exist(self):
        self.assertNotEqual('The living space does not exist!',
                            self.facility.allocate_living(Fellow))

    def test_livingspace_is_full(self):
        self.assertNotEqual('All living spaces are full!',
                            self.facility.allocate_living(Staff))

    def test_person_not_found(self):
        self.assertEqual('Person with id 1313434 not Found!',
                         self.facility.reallocate_person(1313434, 'home'))

    def test_room_not_found(self):
        self.assertEqual('Room not found!',
                         self.facility.reallocate_person('john', 'dojo'))

    # def test_room_to_reallocate_not_found(self):
    #     self.assertEqual('Room to reallocate not Found!',
    #                      self.facility.reallocate_person(4309687600, 'nania'))

    def test_reallocation_to_a_different_room(self):
        person = self.facility.all_persons[0]
        self.facility.create_room('office', 'grey')
        self.facility.reallocate_person(person.identifier, 'grey')
        self.assertEqual(person.current_office.room_name, 'grey')

    def test_reallocation_to_the_same_room(self):
        person = self.facility.all_persons[0]
        return_message = self.facility.reallocate_person(person.identifier, person.current_office)
        self.assertEqual("Reallocations cannot be done to the same room!", return_message)


    def test_room_is_filled(self):
        self.assertEqual('Room is Filled to capacity!',
                         self.facility.reallocate_person())

    def test_data_successfully_exported_to_database(self):
        self.assertEqual('Data successfully exported to Database',
                         self.facility.save_state())

    def test_data_loaded_from_database(self):
        self.assertEqual('Successfully loaded data from the Database!',
                         self.facility.load_state())



