from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup_view'),
    path('email_available', views.email_available, name='email_available'),
    path('login/', views.login_view, name='login_view'),

    path('profile/', views.profile_manager, name='profile_manager'),
    path('profile/update/personal_info/', views.update_personal_info, name='update_personal_info'),
    path('profile/update/profile_picture/', views.update_profile_picture, name='update_profile_picture'),

    path('logout/', views.logout_view, name='logout_view'),

]