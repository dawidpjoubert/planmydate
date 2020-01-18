# Generated by Django 2.2.6 on 2019-11-19 21:22

import activities.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityDistrictDistance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postcode', activities.models.PlainTextField(max_length=4)),
                ('distance', models.DecimalField(decimal_places=3, default=None, max_digits=10)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.Activity')),
            ],
        ),
    ]