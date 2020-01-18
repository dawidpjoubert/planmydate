from django.urls import path

from . import views

app_name = 'activities'
urlpatterns = [
    path('', views.index, name='index'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('meal/<int:pk>/', views.MealDetailView.as_view(), name='meal_detail'),
]