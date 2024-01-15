from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("",views.index,name="index"),
    path("hakkinda/",views.about,name="about"),
    path("yardim/",views.help,name="help"),
    path("oyna/",views.game,name="game"),
    path("yarismacilar/",views.competitors,name="competitors"),
]