from django.urls import path
from . import views

app_name = 'qrhome'

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('login_signup/', views.login_signup_view, name='login_signup'), # Login/Signup
    path('logout/', views.user_logout, name='logout'), # Logout
    path('generate/', views.qrcode_generator, name='qrcode_generator'), # QR Code Generation
    path('history/', views.history_view, name='history'),  # Generation History
]