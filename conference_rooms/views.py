from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View

from conference_rooms.models import Room, Reservation


def all_rooms(request):
    if not Room.objects.all():
        return render(request, 'no_rooms.html')
    rooms = Room.objects.all()
    present = datetime.now().date()
    availability = []
    for room in rooms:
        if Reservation.objects.filter(room_id=room.id).filter(date=present):
            availability.append(False)
        else:
            availability.append(True)
    return render(request, 'all_rooms.html', {'rooms': rooms, 'availability': availability})


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


class AddReservationView(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        present = datetime.now().date()
        reservations = Reservation.objects.order_by('date').filter(room_id=id).filter(date__gte=present)
        return render(request, 'add_reservation.html', {'room': room, 'reservations': reservations})

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        present = datetime.now().date()
        reservations = Reservation.objects.order_by('date').filter(room_id=id).filter(date__gte=present)
        date = request.POST.get('date', '')
        present = datetime.now().date()
        date_format = datetime.strptime(date, "%Y-%m-%d").date()
        comment = request.POST.get('comment', '')
        if Reservation.objects.filter(room_id=id).filter(date=present):
            komunikat = 'Room is not available on this day'
        elif date and date_format >= present:
            komunikat = 'Reservation added'
            if comment != '':
                Reservation.objects.create(date=date, comment=comment, room_id=room.id)
            else:
                Reservation.objects.create(date=date, room_id=room.id)
            return redirect('/main/', {"komunikat": komunikat})
        else:
            komunikat = 'Choose the right day'
        return render(request, 'add_reservation.html',
                      {'komunikat': komunikat, 'room': room, 'reservations': reservations})


def room(request, id):
    room = Room.objects.get(pk=id)
    reservations = Reservation.objects.order_by('date').filter(room_id=id)
    return render(request, 'room.html', {'room': room, 'reservations': reservations})




# Widok powinien zwrócić listę wolnych sal. Jeśli nie znajdzie żadnej, powinien pojawić się komunikat „Brak wolnych sal dla podanych kryteriów wyszukiwania”.

def search_room(request):
    if request.method == 'POST':
        rooms = Room.objects.all()
        name = request.POST.get('name', '')
        min_capacity = request.POST.get('capacity', 0)
        present = datetime.now().date()
        if min_capacity == '':
            min_capacity = 0
        projector = request.POST.get('projector', False)
        rooms = rooms.filter(name__icontains=name)
        rooms = rooms.filter(capacity__gte=min_capacity)
        if projector == 'on':
            rooms = rooms.filter(projector=True)
        rooms = rooms.exclude(reservation__date=present)
        return render(request, "search.html", {'rooms':rooms})