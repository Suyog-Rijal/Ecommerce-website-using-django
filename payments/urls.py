from django.urls import path

from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]