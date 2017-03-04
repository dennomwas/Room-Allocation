# TESTS TO CREATE NEW ROOM

# # assert a room has been created
# # assert room is an office
# # assert room is a living space
# # assert max capacity for office is 6
# # assert max capacity for living space is 4
# assert no duplicate room can be created


# TESTS TO ADD NEW PERSON

# # assert person has been created
# assert person is a fellow
# assert person is a staff
# assert no duplicate person can be created
# assert person list is incrementing

# TEST TO ALLOCATE ROOM

# assert rooms are available
# assert person cannot be allocated more than once



# TEST TO REALLOCATE A ROOM

# assert rooms are available
# assert person moved to new room
# assert person not in previous room


# TEST TO PRINT ALLOCATIONS

# assert room has person allocated
# assert path to txt file

# TEST TO PRINT UNALLOCATED

# assert room has no person assigned
# assert path to txt file


# TEST TO PRINT ROOM

# assert room has people


# TEST TO SAVE STATE TO DB

# assert connection to db


# TEST TO LOAD STATE FROM A DB

# assert connection to db


all_rooms = ['me','u','y','t',1]
for rooms in all_rooms:
    if 'u' not in all_rooms:
        print('found')
    else:
        print('nothing')
