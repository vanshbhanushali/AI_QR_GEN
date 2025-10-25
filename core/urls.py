from django.contrib import admin
from django.urls import path, include # Import 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # ----------------------
    # Include the URLs from the qrhome app
    path('', include('qrhome.urls', namespace='qrhome')),
    # ----------------------
]