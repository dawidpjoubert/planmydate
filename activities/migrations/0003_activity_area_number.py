# Generated by Django 2.2.6 on 2020-02-04 22:32

import activities.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_activitydistrictdistance'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='area_number',
            field=activities.models.AreaField(choices=[(1, 'Central (East)'), (2, 'Central (West)'), (3, 'East'), (4, 'West'), (5, 'Southeast'), (6, 'Southwest'), (7, 'North'), (8, 'Northwest')], default=1),
            preserve_default=False,
        ),
    ]
