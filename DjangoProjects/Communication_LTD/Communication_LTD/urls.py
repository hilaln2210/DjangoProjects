from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('accounts.urls')),  # Redirect home to accounts app
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),

]
