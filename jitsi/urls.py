from django.contrib import admin
from django.urls import path, include

from account.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('home/', home, name='home')
]