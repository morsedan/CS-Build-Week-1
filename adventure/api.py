from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

size = 15  # TODO figure out how to derive this from the rooms
all_rooms = Room.objects.all()
all_rooms = list(all_rooms)
all_rooms.sort(key=lambda x: x.room_id)
room_arr_temp = []
room_arr = []
row_count = 0
for room in all_rooms:
    if room.n_to or room.s_to or room.w_to or room.e_to:
        room_arr_temp.append(1)
    else:
        room_arr_temp.append(0)
    row_count += 1
    if row_count == size:
        row_count = 0
        room_arr.append(room_arr_temp)
        room_arr_temp = []
        row_count == 1

room_dicts = []
for room in all_rooms:
    room_dict = {}
    room_dict['room_id'] = room.room_id
    room_dict['title'] = room.title
    room_dict['description'] = room.description
    room_dict['n_to'] = room.n_to
    room_dict['s_to'] = room.s_to
    room_dict['e_to'] = room.e_to
    room_dict['w_to'] = room.w_to
    room_dicts.append(room_dict)

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse(
        {'uuid': uuid, 'name': player.user.username, 'title': room.title, 'description': room.description,
         'players': players, 'x': player.currentRoom % 15 - 1, 'y': player.currentRoom // 15}, safe=True)


@api_view(["GET"])
def world(request):
    # new_arr = [[1 if i else 0 for i in item] for item in room_grid]
    return JsonResponse({'room_grid': room_arr})

@api_view(["GET"])
def rooms(request):
    return JsonResponse({'rooms': room_dicts})

# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = request.data  # json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(room_id=nextRoomID)
        player.currentRoom = nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name': player.user.username, 'title': nextRoom.title, 'description': nextRoom.description,
                             'players': players, 'error_msg': ""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse(
            {'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players,
             'error_msg': "You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)
