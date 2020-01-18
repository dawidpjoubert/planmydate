from djmoney.models.fields import MoneyField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

# name	outdoor	price	active	intimacy	area	day	type	headline	description_tips	address	link	photo	price_sign	fire	book_ahead	pass_day	score	include
# Tate Modern	0	1	0	1		1	museum	Enjoy modern art and have a drink on the rooftop at the Tate Modern	Tate Modern is perfect for a casual date enjoying modern art, and in addition to the free exhibits there are usually great paid shows on display. Visit the top floor of the Blavatnik building for a 360 London skyline view at the bar/cafe. Visitors aged 16-25 can join the Tate Collective for £5 exhibition tickets.	Tate Modern, Bankside, London SE1 9TG	https://www.tate.org.uk/visit/tate-modern		£	☹	No	1	2	1
# Tate Britain	0	1	0	1		1	museum	Enjoy art at the Tate Britain	Not available	Tate Britain, Millbank, Westminster, London SW1P 4RG	https://www.tate.org.uk/visit/tate-britain		£	☹	No	1	2	1
# V&A Museum	0	1	0	1		1	museum	Check out some art and design at the V&A museum	The Victoria & Albert museum has a collection of over 2 million objects - visit to learn about art and design and see exhibits that in the past have ranged from food to top fashion.	V&A Museum, Cromwell Road, London SW7 2RL	https://www.vam.ac.uk/		£	☹	No	1	2	1

# Creating a class allows us to identify fields that are meant to be raw HTML as all TextField instances are probably treated as UNICODE and then HTML encoded all the way. Where as a
# HtmlField we assume is a UNICODE blob of HTML that we can print directly to screen. The only time we will encode it is if we put it into a form for the user to edit.

class HtmlBlob(models.TextField):
    pass


class PlainTextField(models.CharField):
    pass

class TimeOfDayField(models.IntegerField):
    TOD_DAY_ONLY = 1
    TOD_NIGHT_ONLY = 2
    TOD_DAY_OR_NIGHT = 3
    TOD_CHOICES = (
        (TOD_DAY_OR_NIGHT, _('Open early til late')),
        (TOD_DAY_ONLY, _('Open in the day only')),
        (TOD_NIGHT_ONLY, _('Open at night only')),
    )

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.min_value, self.max_value = 1, 3
        kwargs['blank'] = False
        kwargs['choices'] = self.TOD_CHOICES
        kwargs['default'] = self.TOD_DAY_OR_NIGHT
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)


class StarRatingField(models.IntegerField):
    STAR_NULL = None
    STAR_1 = 1
    STAR_2 = 2
    STAR_3 = 3
    STAR_4 = 4
    STAR_5 = 5
    STAR_CHOICES = (
        (STAR_NULL, _('Unrated')),
        (STAR_1, _('1 Star')),
        (STAR_2, _('2 Star')),
        (STAR_3, _('3 Star')),
        (STAR_4, _('4 Star')),
        (STAR_5, _('5 Star')),
    )

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.min_value, self.max_value = 1, 5
        kwargs['blank'] = True
        kwargs['choices'] = self.STAR_CHOICES
        kwargs['default'] = self.STAR_NULL
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)


class PriceRatingField(models.IntegerField):
    PRICE_FREE = 1
    PRICE_LOW = 2
    PRICE_MEDIUM = 3
    PRICE_HIGH = 4
    PRICE_EXTREME = 5
    PRICE_CHOICES = (
        (PRICE_FREE, _('Free')),
        (PRICE_LOW, _('Low Price')),
        (PRICE_MEDIUM, _('Medium Price')),
        (PRICE_HIGH, _('High Price')),
        (PRICE_EXTREME, _('Premium Price')),
    )

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.min_value, self.max_value = 1, 5
        kwargs['blank'] = False
        kwargs['choices'] = self.PRICE_CHOICES
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)


class CardioLevelField(models.IntegerField):
    LEVEL_NONE = 1
    LEVEL_LOW = 2
    LEVEL_MILD = 3
    LEVEL_ACTIVE = 4
    LEVEL_VERY_ACTIVE = 5
    LEVEL_CHOICES = (
        (LEVEL_NONE, _('None / Inactive')),
        (LEVEL_LOW, _('Low level of cardio')),
        (LEVEL_MILD, _('Mild level of cardio')),
        (LEVEL_ACTIVE, _('Some cardio / active')),
        (LEVEL_VERY_ACTIVE, _('High level / Very active cardio')),
    )

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.min_value, self.max_value = 1, 5
        kwargs['blank'] = False
        kwargs['choices'] = self.LEVEL_CHOICES
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)



# class LikertField(models.IntegerField):
#     LIKERT_NO = 1
#     LIKERT_MAYBE_NO = 2
#     LIKERT_NULL = 3
#     LIKERT_MAYBE_YES = 4
#     LIKERT_YES = 5
#     LIKERT_CHOICES = (
#         (LIKERT_NO, _('Hard no')),
#         (LIKERT_MAYBE_NO, _('Weak no')),
#         (LIKERT_NULL, _('Unsure / Null')),
#         (LIKERT_MAYBE_YES, _('Weak yes')),
#         (LIKERT_YES, _('Strong yes')),
#     )
#
#     def __init__(self, verbose_name=None, name=None, **kwargs):
#         self.min_value, self.max_value = 1, 5
#         kwargs['blank'] = False
#         kwargs['choices'] = self.LIKERT_CHOICES
#         kwargs['default'] = self.LIKERT_NULL
#         models.IntegerField.__init__(self, verbose_name, name, **kwargs)
#

class YesNoField(models.IntegerField):
    OPTION_YES = 1
    OPTION_NO = 2
    OPTION_CHOICES = (
        (OPTION_YES, _('Yes')),
        (OPTION_NO, _('No')),
    )

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.min_value, self.max_value = 1, 2
        kwargs['blank'] = False
        kwargs['choices'] = self.OPTION_CHOICES
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)


class BookingRequiredField(models.IntegerField):
    OPTION_YES = 1
    OPTION_NO = 2
    OPTION_RECOMMENDED = 3
    OPTION_CHOICES = (
        (OPTION_NO, _('No')),
        (OPTION_RECOMMENDED, _('Recommended')),
        (OPTION_YES, _('Yes')),
    )

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.min_value, self.max_value = 1, 3
        kwargs['blank'] = False
        kwargs['choices'] = self.OPTION_CHOICES
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)


class IntimateField(models.IntegerField):
    INTIMATE_LOW = 1
    INTIMATE_MEDIUM = 2
    INTIMATE_HIGH = 3
    
    INTIMATE_CHOICES = (
        (INTIMATE_LOW, _('Casual & Relaxed')),
        (INTIMATE_MEDIUM, _('Cosy & Intimate')),
        (INTIMATE_HIGH, _('Sexy & Romantic')),
    )

    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.min_value, self.max_value = 1, 3
        kwargs['blank'] = False
        kwargs['choices'] = self.INTIMATE_CHOICES
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)


class ActivityType(models.Model):
    name = models.CharField(max_length=64)


class Activity(models.Model):
    CLASS_EVENT = 'Event'
    CLASS_MEAL = 'Meal'
    CLASS_OTHER = 'Unknown thing'
    CLASS_CHOICES = (
        (CLASS_EVENT, _(CLASS_EVENT)),
        (CLASS_MEAL, _(CLASS_MEAL)),
        (CLASS_OTHER, _(CLASS_OTHER)),
    )

    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=128, verbose_name=_('Slug'))
    headline = models.CharField(max_length=128, blank=True)
    description_html = HtmlBlob(blank=True)
    address_text = PlainTextField(max_length=2048, blank=True)
    address_postcode = PlainTextField(max_length=10, blank=True)
    address_latitudinal = models.DecimalField(max_digits=12, decimal_places=8, default=None)
    address_longitudinal = models.DecimalField(max_digits=12, decimal_places=8, default=None)
    external_link = models.URLField(max_length=1024, blank=True)
    price_rating = PriceRatingField()
    is_outdoor = YesNoField()
    intimate = IntimateField()
    booking_required = BookingRequiredField()
    time_of_day = TimeOfDayField()
    # rating = StarRatingField() #  must be calculated
    # area TBC - Use spatial library https://realpython.com/location-based-app-with-geodjango-tutorial/

    def __str__(self):
        return self.name.__str__()


class ActivityDistrictDistance(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    postcode = PlainTextField(max_length=4, blank=False)
    distance = models.DecimalField(max_digits=10, decimal_places=3, default=None) # Kilometers


class EventActivity(Activity):
    TYPE_MUSEUM = 'Museum'
    TYPE_MUSIC = 'Music'
    TYPE_OUTDOOR = 'Outdoor'
    TYPE_ACTIVITY = 'Activity'
    TYPE_MARKET = 'Market'
    TYPE_SPORT = 'Sport'
    TYPE_HOBBY = 'Hobby'
    TYPE_TOUR = 'Tour'
    TYPE_COMEDY = 'Comedy'
    TYPE_THEATRE = 'Theatre'
    TYPE_OTHER = 'Other Event'
    TYPE_CHOICES = (
        (TYPE_MUSEUM, _(TYPE_MUSEUM)),
        (TYPE_MUSIC, _(TYPE_MUSIC)),
        (TYPE_OUTDOOR, _(TYPE_OUTDOOR)),
        (TYPE_ACTIVITY, _(TYPE_ACTIVITY)),
        (TYPE_MARKET, _(TYPE_MARKET)),
        (TYPE_SPORT, _(TYPE_SPORT)),
        (TYPE_HOBBY, _(TYPE_HOBBY)),
        (TYPE_TOUR, _(TYPE_TOUR)),
        (TYPE_COMEDY, _(TYPE_COMEDY)),
        (TYPE_THEATRE, _(TYPE_THEATRE)),
        (TYPE_OTHER, _(TYPE_OTHER)),
    )

    event_type = models.CharField(max_length=32, choices=TYPE_CHOICES, default=TYPE_OTHER, blank=False)
    is_cardio = CardioLevelField()

class MealActivity(Activity):
    TYPE_BAR = 'Bar'
    TYPE_RESTAURANT = 'Restaurant'
    TYPE_CAFE = 'Cafe'
    TYPE_PICNIC = 'Picnic'
    TYPE_OTHER = 'Other Meal'
    TYPE_CHOICES = (
        (TYPE_BAR, _(TYPE_BAR)),
        (TYPE_RESTAURANT, _(TYPE_RESTAURANT)),
        (TYPE_CAFE, _(TYPE_CAFE)),
        (TYPE_PICNIC, _(TYPE_PICNIC)),
        (TYPE_OTHER, _(TYPE_OTHER)),
    )

    meal_type = models.CharField(max_length=32, choices=TYPE_CHOICES, default=TYPE_OTHER, blank=False)
