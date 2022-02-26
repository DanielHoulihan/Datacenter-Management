from django.urls import  path
from . import views

urlpatterns = [
    path('', views.datacenters, name = "datacenters"),
    path('budget/',views.budget, name = "budget"),
    path('configure/',views.configure, name = "configure"),
    path('tco/',views.tco, name = "tco"),
    path('floors/',views.floors, name = "floors"),
    path('floors/<floorid>/racks',views.racks, name = "racks"),
    path('floors/<floorid>/racks/<rackid>/hosts',views.hosts, name = "hosts"),
    path('floors/<floorid>/racks/<rackid>/hosts/<hostid>',views.host_activity, name = "host_activity"),
]