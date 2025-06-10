from django.urls import path
from . import views

urlpatterns = [
        path('', views.view_bag, name='view_bag'),
    path('add/<slug:slug>/', views.add_to_bag, name='add_to_bag'),
    path('remove/<str:key>/', views.remove_from_bag, name='remove_from_bag'),
    path('update/<str:key>/', views.update_quantity, name='update_quantity'),
]