class Room(object):

    def __init__(self, room_name, room_type):
        self.room_name = room_name
        self.room_type = room_type


class Office(Room):

    def __init__(self, room_name):
        self.max_capacity = 6
        super(Office, self).__init__(room_name)
        self.room_type = 'Office'
        self.persons_allocated = []


class LivingSpace(Room):

    def __init__(self, room_name):
        self.max_capacity = 4
        super(LivingSpace, self).__init__(room_name)
        self.room_type = 'Living Space'
        self.fellows_allocated = []

