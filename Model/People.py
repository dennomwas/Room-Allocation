from abc import ABCMeta, abstractmethod


class Person(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, first_name, last_name, current_office=None):
        self.first_name = first_name
        self.last_name = last_name
        self.current_office = current_office
        self.identifier = id(self)


class Staff(Person):

    def __init__(self, *args, **kwarg):

        super(Staff, self).__init__(*args, **kwarg)
        self.person_type = "STAFF"

    def __str__(self):
        return '{} {} {} {}'.format(self.identifier, self.first_name,
                                    self.last_name, self.person_type)


class Fellow(Person):

    def __init__(self, *args, accommodation_request=None):

        super(Fellow, self).__init__(*args)
        self.accommodation_request = accommodation_request
        self.current_living = None
        self.person_type = "FELLOW"

    def __str__(self):
        return '{} {} {} {}'.format(self.identifier, self.first_name,
                                    self.last_name, self.person_type)

