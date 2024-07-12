# Generated by Django 5.0.6 on 2024-07-09 14:09

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibrarianUser',
            fields=[
                ('baseauthmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('librarian_id', models.CharField(editable=False, max_length=10, unique=True)),
                ('librarian_name', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
            ],
            options={
                'verbose_name': ('Librarian User',),
                'verbose_name_plural': 'Librarian Users',
            },
            bases=('Users.baseauthmodel',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
