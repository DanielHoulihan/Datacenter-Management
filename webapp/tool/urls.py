from django.urls import  path
from . import views

urlpatterns = [
    path('', views.get_datacenters, name = "get_datacenters"),
    path('floors/',views.floors, name = "floors"),
    path('floors/<floorid>/racks',views.racks, name = "racks"),
    path('floors/<floorid>/racks/<rackid>/hosts',views.hosts, name = "hosts"),
    path('floors/<floorid>/racks/<rackid>/hosts/<hostid>',views.host_activity, name = "host_activity"),
]