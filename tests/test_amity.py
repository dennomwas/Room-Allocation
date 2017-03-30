import unittest

from Model.Amity import Amity
from Model.People import Staff, Fellow
from Model.Rooms import Office, LivingSpace


class TestAmity(unittest.TestCase):
    def setUp(self):
        self.facility = Amity()

    def test_create_room(self):
        self.facility.create_room('office', 'tsavo')
        self.assertEqual('tsavo already exists!',
                         self.facility.create_room('office', 'tsavo'))

        self.facility.create_room('livingspace', 'red')
        self.assertEqual('red already exists!',
                         self.facility.create_room('livingspace', 'red'))

    def test_file_not_loaded(self):
        self.assertEqual('File not found, Please try again...',
                         self.facility.load_people('files/not_loaded.txt'))

    def test_file_exported(self):
        self.assertEqual('Successfully exported room allocations to export.txt',
                         self.facility.print_allocations('export.txt'))

    def test_print_room(self):
        self.assertEqual('room name not found',
                         self.facility.print_room('dojo'))

    def test_livingspace_does_not_exist(self):
        self.assertEqual('The living space does not exist!',
                            self.facility.allocate_living(Fellow))

    def test_livingspace_is_full(self):
        self.assertNotEqual('All living spaces are full!',
                            self.facility.allocate_living(Staff))

    def test_person_not_found(self):
        self.facility.add_person('John', 'Snow', 'fellow', 'y')
        self.assertEqual('Person with id 1313434 not Found!',
                         self.facility.reallocate_person(1313434, 'home'))

    def test_room_not_found(self):
        self.assertEqual('Room not found!',
                         self.facility.reallocate_person('john', 'dojo'))


    def test_data_successfully_exported_to_database(self):
        self.assertEqual('Data successfully exported to Database',
                         self.facility.save_state('data'))

    def test_data_loaded_from_database(self):
        self.assertEqual('Successfully loaded data from the Database!',
                         self.facility.load_state('data'))



