from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('blogs.urls')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/blogs/', include('blogs.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)