from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='users'

urlpatterns = [
    path('login/',views.login,name='login'),
    path('registration/',views.registration,name='registration'),
    path('profile',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('googleauth/',views.google_auth,name='googleauth'),
    path('googlelogin/',views.google_login,name='googlelogin'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html'),name='password_change'),
    path('password_change_done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
]
