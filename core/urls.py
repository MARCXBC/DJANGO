"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# FIX: Added 'login' to the end of the view function import statement block
from subfolder.views import hello, mail_user, login 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello),
    path('mail/', mail_user),
    path('api/login/', login), # This will now resolve perfectly!
    path("api/accounts/", include("subfolder.urls")),
    path("api/blogs/", include("blog.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
