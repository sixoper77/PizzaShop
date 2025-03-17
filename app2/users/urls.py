from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('googleauth/', views.google_auth, name='googleauth'),
    path('googlelogin/', views.google_login, name='googlelogin'),
    path('password_change/', views.PasswordChangeView.as_view(template_name='registration/change-password.html'),name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    # path('reset_password/', auth_views.PasswordResetView.as_view(),name='reset_password'),
    
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
]