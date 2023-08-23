
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from login.views import LoginFormView
from setting import settings

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('login/', include('login.urls')),
    path('admin/'
         '', admin.site.urls),
    path('asys/', include('app.urls')),


    # path('', include('django.contrib.auth.urls'), name='login'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)