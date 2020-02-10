from django import forms
from .models import CardioLevelField, PriceRatingField, IntimateField, BookingRequiredField, YesNoField, TimeOfDayField, AreaField



class CriteriaForm(forms.Form):
    blank_choice = ((None, 'Any'),)

    # Area is not blank, we force a choice on the user. Other options can be blank
    area_number = forms.ChoiceField(choices=AreaField.AREA_CHOICES, label="Area", required=False)

    is_outdoor = forms.ChoiceField(choices=blank_choice + YesNoField.OPTION_CHOICES, label='Outdoors', required=False)
    #time_of_day = forms.ChoiceField(choices=blank_choice + TimeOfDayField.TOD_CHOICES, label='Day / Night', required=False)
    price_rating = forms.ChoiceField(choices=blank_choice + PriceRatingField.PRICE_CHOICES, label="Budget", required=False)
    cardio = forms.ChoiceField(choices=blank_choice + CardioLevelField.LEVEL_CHOICES, label="Max Energy", required=False)
    intimate = forms.ChoiceField(choices=blank_choice + IntimateField.INTIMATE_CHOICES, label="Max Intimacy", required=False)

