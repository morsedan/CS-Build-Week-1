import sys

sys.path.append('/Users/morse/dev/CS28-Sprint4/CS-Build-Week-1/adventure/')
from adventure.models import Room as DjangoRoom

from random import randint

from make_room_titles import text_gen

class Room:
    def __init__(self, id):
        self.id = id
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.is_accessible = True
        self.title = None
        self.description = None

class RoomGen:
    def __init__(self):
        self.rooms = []

    def create_rooms(self, width=10, height=10):
        """
        [1, 2, 3, 4, 5,
         6, 7, 8, 9, 10,
         11,12,13,14,15,
         16,17,18,19,20,
         21,22,23,24,25,]
        """
        # create blank rooms
        rooms = [Room(id) for id in range(1, (width * height + 1))]

        # make some rooms inaccessible
        for _ in range(0, height * width // 10):
            rand_num = randint(0, height * width - 1)
            while rooms[rand_num].is_accessible == False:
                rand_num = randint(0, height * width - 1)
            rooms[rand_num].is_accessible = False

        # set each room's directions
        for i in range(len(rooms)):
            room = rooms[i]
            rand_title, rand_description = text_gen()
            room.title = rand_title
            room.description = rand_description
            
            n_index = i - width
            s_index = i + width
            e_index = i + 1
            w_index = i - 1

            if not rooms[i].is_accessible:
                continue

            if n_index >= 0:
                if rooms[n_index].is_accessible:
                    room.n_to = n_index + 1
            if s_index < height * width:
                if rooms[s_index].is_accessible:
                    room.s_to = s_index + 1
            if e_index % width != 0 and e_index < len(rooms):
                if rooms[e_index].is_accessible:
                    room.e_to = e_index + 1
            if i % width != 0:
                if rooms[w_index].is_accessible:
                    room.w_to = w_index + 1

            # now add to the description text 
            exits = []
            if room.n_to:
                exits.append("north")
            if room.s_to:
                exits.append("south")
            if room.w_to:
                exits.append("west")
            if room.e_to:
                exits.append("east")

            exits_text = ''
            if len(exits) == 0:
                pass
            elif len(exits)>2:
                for i in exits[:-1]:
                    exits_text += i + ", "
                exits_text += (f'and {exits[-1]}')
            elif len(exits) == 2:
                exits_text += exits[0] + " and " + exits[1]
            else:
                exits_text += exits[0]
            
            if len(exits) == 1:
                room.description += f"There is an exit to the {exits_text}"
            else:
                room.description += f"There are exits to the {exits_text}"

        # put rooms into rows
        rooms_in_rows = []

        start_index = 0
        for _ in range(height):
            row = rooms[start_index:start_index + width]
            start_index += width
            rooms_in_rows.append(row)

        self.rooms = rooms_in_rows

    def create_django_rooms(self):

        # get each room
        # turn into a django room
        # save to DB
        for row in self.rooms:
            for room in row:
                if room:
                    django_room = DjangoRoom()
                    django_room.room_id = room.id
                    django_room.title = room.title
                    django_room.description = room.description
                    if room.n_to:
                        django_room.n_to = room.n_to
                    if room.s_to:
                        django_room.s_to = room.s_to
                    if room.e_to:
                        django_room.e_to = room.e_to
                    if room.w_to:
                        django_room.w_to = room.w_to
                    django_room.save()

rg = RoomGen()
rg.create_rooms(15,15)
# used to print and check the generator
# for i in rg.rooms:
#     for room in i:
#         print(room.title,'\n',room.description,'\n')

# used to update the file (when this file is imported from the manage.py shell env)
rg.create_django_rooms()

# confirmation message
print(f"Created {len(rg.rooms)} * {len(rg.rooms[0])} rooms.")