from django.urls import  path
from . import views

urlpatterns = [
    path('', views.configure, name = "configure"),
    # path('<sub_id>/', views.select, name='select'),
    path('budget/',views.budget, name = "budget"),
    path('tco/',views.tco, name = "tco"),
    path('floors/',views.floors, name = "floors"),
    path('floors/<floorid>/racks',views.racks, name = "racks"),
    path('floors/<floorid>/racks/<rackid>/hosts',views.hosts, name = "hosts"),
]