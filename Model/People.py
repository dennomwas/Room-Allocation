
class Person(object):

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Staff(Person):

    def __init__(self, first_name, last_name):
        super(Staff, self).__init__(first_name, last_name)
        self.designation = 'Staff'
        self.current_occupancy = []
        self.identifier = id(self)


class Fellow(Person):

    def __init__(self, first_name, last_name, accommodation_request='n'):
        super(Fellow, self).__init__(first_name, last_name)
        self.accommodation_request = accommodation_request
        self.designation = 'Fellow'
        self.current_occupancy = []
        self.identifier = id(self)







