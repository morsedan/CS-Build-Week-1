import sys

sys.path.append('/Users/morse/dev/CS28-Sprint4/CS-Build-Week-1/adventure/')
from adventure.models import Room as DjangoRoom

sys.path.append('/Users/morse/dev/CS28-Sprint4/CS-Build-Week-1/util/')
from sample_generator import Room

class RoomGenerator:
    def __init__(self):
        self.rooms = None
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x=11, size_y=11, num_rooms=100):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''
        # return a 0/1 version of this grid thats generated to
        # Front end.
        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west

        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            # Create a room in the given direction
            room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            self.grid[y][x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)

            # Update iteration variables
            previous_room = room
            room_count += 1


    def create_django_rooms(self):

        # get each room
        # turn into a django room
        # save to DB
        for row in self.grid:
            for room in row:
                if room:
                    django_room = DjangoRoom()
                    django_room.title = room.name
                    django_room.description = room.description
                    if room.n_to:
                        django_room.n_to = room.n_to.id
                    if room.s_to:
                        django_room.s_to = room.s_to.id
                    if room.e_to:
                        django_room.e_to = room.e_to.id
                    if room.w_to:
                        django_room.w_to = room.w_to.id
                    django_room.save()

#  This is what to run in the manage.py python shell:
#
# from room_gen import RoomGenerator
# rg = RoomGenerator()
# rg.generate_rooms()
# rg.create_django_rooms()