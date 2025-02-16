from django.urls import path
from . import views

app_name='users'

urlpatterns = [
    path('login/',views.login,name='login'),
    path('registration/',views.registration,name='registration'),
    path('profile',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('googleauth/',views.google_auth,name='googleauth'),
    path('googlelogin/',views.google_login,name='googlelogin'),
]
