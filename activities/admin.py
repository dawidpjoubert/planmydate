from django.contrib import admin

# Register your models here.
from .models import EventActivity, MealActivity


@admin.register(MealActivity)
class MealActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_rating', 'is_outdoor', 'intimate', 'booking_required', 'time_of_day', 'meal_type', 'area_number')

@admin.register(EventActivity)
class EventActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_rating', 'is_outdoor', 'intimate', 'is_cardio', 'booking_required', 'time_of_day', 'event_type', 'area_number')
    #fields = () # List of fields on details / form editing
    #exclude = ('birth_date',) fields to specifically exclude

