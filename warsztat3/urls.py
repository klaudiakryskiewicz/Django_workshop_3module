"""warsztat3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from conference_rooms import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', views.all_rooms),
    path('room/<int:id>', views.room),
    path('room/new/', views.AddRoomView.as_view()),
    path('room/delete/<int:id>', views.DeleteRoomView.as_view()),
    path('room/modify/<int:id>', views.ModifyRoomView.as_view()),
    path('room/reserve/<int:id>', views.AddReservationView.as_view()),
    path('search/', views.search_room)
]
