from django.urls import  path
from . import views

urlpatterns = [
    path('', views.get_reports, name = "get_reports"),
    path('reports/<int:id>/',views.report_detail, name = "report_detail"),
    path('reports/<int:id>/hosts/<int:Id2>',views.host_detail, name = "host_detail")
]