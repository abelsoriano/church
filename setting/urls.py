
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from login.views import *
from setting import settings

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', include('login.urls')),
    path('admin/''', admin.site.urls),
    path('asys/', include('app.urls')),
]

handler404 = 'login.views.handler404'
handler500 = 'login.views.handler500'
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)