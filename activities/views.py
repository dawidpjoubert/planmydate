import random
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views import generic
from haversine import haversine, Unit


from .models import EventActivity, MealActivity, ActivityDistrictDistance
from .models import CardioLevelField, PriceRatingField, IntimateField, BookingRequiredField, YesNoField, TimeOfDayField
from .forms import CriteriaForm


def index(request):
    events_list = EventActivity.objects.order_by("?")[:10]
    meals_list = MealActivity.objects.order_by("?")[:10]
    context_date = {}
    date_generated = False

    form = CriteriaForm(request.GET or None)

    if 'submit' in request.GET and form.is_valid():
        (date_generated, context_date) = process_form(form, force_id = request.GET.get("force_id", None))


    context = {
        'events_list': events_list,
        'meals_list': meals_list,
        'error_message': "",
        'form': form,
        'date': context_date,
        'date_generated': date_generated,
    }

    return render(request, 'home/index.html', context)

def process_form(form, force_id = None):
    context = {}

    # Filter to get an appropriate event within 2km of the selected post code
    # Filter to get an appropriate meal within 2km of the selected post code
    max_distance = 1.0  # Kilometers
    ids = list(ActivityDistrictDistance.objects.filter(postcode__exact=form.cleaned_data['area'],
                                                       distance__lte=max_distance).values_list('activity_id',
                                                                                               flat=True))
    count_events_area = EventActivity.objects.filter(id__in=ids).count()
    count_meals_area = MealActivity.objects.filter(id__in=ids).count()

    # Validate the area selected to see if we have found options for it
    if not count_events_area:
        form.add_error("area", "No event options found for this area")
    if not count_meals_area:
        form.add_error("area", "No meals options found for this area")

    # If no results at this point we cannot continue and we return failed
    if not form.is_valid():
        return (False, context)

    # Queryset for our filter construction
    selected_event_query = EventActivity.objects.filter(id__in=ids)
    selected_meal_query = MealActivity.objects.filter(id__in=ids)

    if form.cleaned_data['is_outdoor']:
        selected_event_query = selected_event_query.filter(is_outdoor=form.cleaned_data['is_outdoor'])
        #Removed until data is ready - selected_meal_query = selected_meal_query.filter(is_outdoor=form.cleaned_data['is_outdoor'])
    if form.cleaned_data['time_of_day']:
        selected_event_query = selected_event_query.filter(time_of_day=form.cleaned_data['time_of_day'])
        selected_meal_query = selected_meal_query.filter(time_of_day=form.cleaned_data['time_of_day'])
    if form.cleaned_data['price_rating']:
        if form.cleaned_data['price_rating'] == PriceRatingField.PRICE_FREE.__str__():
            selected_event_query = selected_event_query.filter(price_rating=form.cleaned_data['price_rating'])
            # There is no such thing as a free-meal :-)
            selected_meal_query = selected_meal_query.filter(price_rating__lte=PriceRatingField.PRICE_LOW)
        else:
            selected_event_query = selected_event_query.filter(price_rating__lte=form.cleaned_data['price_rating'])
            selected_meal_query = selected_meal_query.filter(price_rating__lte=form.cleaned_data['price_rating'])
    if form.cleaned_data['intimate']:
        selected_event_query = selected_event_query.filter(intimate__lte=form.cleaned_data['intimate'])
        #Removed until data is ready - selected_meal_query = selected_meal_query.filter(intimate=form.cleaned_data['intimate'])
    if form.cleaned_data['cardio']:
        selected_event_query = selected_event_query.filter(is_cardio__lte=form.cleaned_data['cardio'])
        # Meals don't have cardio

    # Finally hit the database hard!
    count_events = selected_event_query.count()
    count_meals = selected_meal_query.count()

    if not count_events:
        form.add_error("area", "No event options found for restrictive filtering. Ease up your criteria")

    if not count_meals:
        form.add_error("area", "No meal options found for restrictive filtering. Ease up your criteria")

    # If no results at this point we cannot continue and we return failed
    if not form.is_valid():
        return (False, context)

    # The force_id below allows us to pass in filter criteria but pre-select a specific meal or event
    # which kind of 'locks that thing in'. So we select that specific thing (if a force id is passed in)
    selected_event = None
    selected_meal = None

    if force_id:
        selected_event = EventActivity.objects.filter(pk=force_id).first()
        selected_meal = MealActivity.objects.filter(pk=force_id).first()

    # No event has been force selected so pick one at random
    if not selected_event:
        selected_event = selected_event_query.order_by("?")[0]

    # No meal has been force selected so pick one at random
    if not selected_meal:
        selected_meal = selected_meal_query.order_by("?")[0]

    distance = haversine((selected_event.address_latitudinal, selected_event.address_longitudinal),
                         (selected_meal.address_latitudinal, selected_meal.address_longitudinal),
                         unit=Unit.KILOMETERS)

    context["count_events_area"] = count_events_area
    context["count_meals_area"] = count_meals_area
    context["count_events"] = count_events
    context["count_meals"] = count_meals
    context["event"] = selected_event
    context["meal"] = selected_meal
    context["distance"] = distance

    return (True, context)

class MealDetailView(generic.DetailView):
    model = MealActivity
    template_name = 'meal_detail.html'


class EventDetailView(generic.DetailView):
    model = EventActivity
    template_name = 'event_detail.html'