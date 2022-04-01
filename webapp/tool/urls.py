from django.urls import  path
from . import views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('', views.configure, name = "configure"),
    # path('<sub_id>/', views.select, name='select'),
    path('budget/',views.budget, name = "budget"),
    path('tco/',views.tco, name = "tco"),
    path('assets/',views.assets, name = "assets"),

]