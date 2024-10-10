from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('calculator/', include('calculator.urls')),
    path('accounts/', include('accounts.urls')),
    path('appointment/', include('appointment.urls')),
    path('advisor/', include('advisor.urls')),
    path('base/', include('base.urls')),
]


# wwww.sanchariray.com/
# 127.0.0.1:8000/
# 127.0.0.1:8000/calculator