class Room(object):

    def __init__(self, room_name):
        self.room_name = room_name


class Office(Room):
    max_capacity = 6

    def __init__(self, room_name):

        super(Office, self).__init__(room_name)
        self.persons_allocated = []

    def __str__(self):
        return self.room_name


class LivingSpace(Room):
    max_capacity = 4

    def __init__(self, room_name):

        super(LivingSpace, self).__init__(room_name)
        self.persons_allocated = []

    def __str__(self):
        return self.room_name
