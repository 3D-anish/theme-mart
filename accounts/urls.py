from django.urls import path
from .views import (
    login_view, register, verify_email, 
    logout_view, change_password, edit_profile, 
    forgot_password, reset_password
)

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('verify-email/', verify_email, name='verify_email'),
    
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('change-password/', change_password, name='change_password'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),
]
