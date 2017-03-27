
class Person(object):

    def __init__(self, first_name, last_name, current_office=None):
        self.first_name = first_name
        self.last_name = last_name
        self.current_office = current_office


class Staff(Person):

    def __init__(self, first_name, last_name, current_occupancy=None):

        super(Staff, self).__init__(first_name, last_name, current_occupancy)
        self.identifier = id(self)


    def __str__(self):
        return '{} {} {}'.format(self.identifier, self.first_name, self.last_name)

    # def __repr__(self):
    #     return str(self.identifier) + ' ' + self.first_name + ' ' + self.last_name

class Fellow(Person):

    def __init__(self, first_name, last_name,
                 current_occupancy=None, accommodation_request=None):

        super(Fellow, self).__init__(first_name, last_name)
        self.accommodation_request = accommodation_request
        self.identifier = id(self)
        self.current_living = None

    def __str__(self):
        return '{} {} {}'.format(self.identifier, self.first_name,
                                    self.last_name)

    #
    # def __repr__(self):
    #     return str(self.identifier) + ' ' + self.first_name + ' ' + self.last_name



# d = Fellow('Dennis', 'Mwangi')
# print(d)
#
# d = Staff('Dennis', 'Mwangi')
#
# print(d)









