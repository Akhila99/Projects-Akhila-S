from django.contrib import admin
from django.urls import path, include
#from django.urls1 import path, include

from django.conf import settings
from django.conf.urls.static import static
#from django.conf.urls1.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plant_app.urls')),
    path('', include('plant_app.urls1')),
    path('api/', include('plant_api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
