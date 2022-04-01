from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path('admin/', admin.site.urls),
    path('tool/', include ('tool.urls')),
    path('', RedirectView.as_view(url='tool/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

