from django.shortcuts import render, redirect
from django.views import View

from conference_rooms.models import Room


def all_rooms(request):
    if not Room.objects.all():
        return render(request, 'no_rooms.html')
    rooms = Room.objects.all()
    return render(request, 'all_rooms.html', {'rooms':rooms})


class AddRoomView(View):
    def get(self, request):
        return render(request, 'add_room.html')

    def post(self, request):
        name = request.POST.get('name', '')
        capacity = request.POST.get('capacity', '')
        projector = request.POST.get('projector', False)
        if projector == 'on':
            projector = True
        else:
            projector = False
        if Room.objects.filter(name=name):
            komunikat = 'This room already exists!'
        elif name and capacity and int(capacity) > 0:
            komunikat = 'Conference room added'
            Room.objects.create(name=name, capacity=capacity, projector=projector)
        else:
            komunikat = 'Wrong input'
        return render(request, 'add_room.html', {"komunikat": komunikat})


class ModifyRoomView(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        projector = 'off'
        if room.projector == True:
            projector = 'checked'
        return render(request, 'add_room.html', {'room': room, 'projector': projector})

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        name = request.POST.get('name', '')
        capacity = request.POST.get('capacity', '')
        projector = request.POST.get('projector', False)
        if projector == 'on':
            projector = True
        else:
            projector = False
        if Room.objects.filter(name=name) and name != room.name:
            komunikat = 'This room already exists!'
        elif name and capacity and int(capacity) > 0:
            komunikat = 'Conference room modified'
            room.name = name
            room.capacity = capacity
            room.projector = projector
            room.save()
            return redirect('/main/', {"komunikat": komunikat})
        else:
            komunikat = 'Wrong input'
        return render(request, 'add_room.html', {"komunikat": komunikat})


class DeleteRoomView(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        return render(request, 'delete_room.html', {'room': room})

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        action = request.POST['action']
        if action == 'yes':
            room.delete()
        return redirect('/main/')

