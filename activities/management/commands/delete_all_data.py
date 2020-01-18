# Run reset.sh to rebuild the database if you also need that done.
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import EventActivity, MealActivity


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        username = 'admin'
        password = 'StatReloader'
        email = 'admin@mail.com'

        if User.objects.filter(username=username).count()==0:
            User.objects.create_superuser(username, email, password)
            print('Superuser created.')
        else:
            print('Superuser creation skipped.')

        EventActivity.objects.all().delete()
        MealActivity.objects.all().delete()

