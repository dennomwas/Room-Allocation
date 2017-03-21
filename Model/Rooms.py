class Room(object):

    def __init__(self, room_name):
        self.room_name = room_name
        # self.room_type = room_type


class Office(Room):
    max_capacity = 6

    def __init__(self, room_name):
        # self.available_spaces = 6
        super(Office, self).__init__(room_name)
        self.room_type = 'office'
        self.persons_allocated = []

    def __str__(self):
        return self.room_name + ' ' + self.room_type


class LivingSpace(Room):
    max_capacity = 4

    def __init__(self, room_name):
        # self.available_spaces = 4
        super(LivingSpace, self).__init__(room_name)
        self.room_type = 'livingspace'
        self.persons_allocated = []

    def __str__(self):
        return self.room_name + ' ' + self.room_type

# d = Office("narnia")
# print(d)
