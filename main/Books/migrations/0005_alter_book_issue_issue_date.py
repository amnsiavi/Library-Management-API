# Generated by Django 5.0.7 on 2024-07-30 09:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0004_alter_book_issue_issue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_issue',
            name='issue_date',
            field=models.DateField(default=datetime.datetime(2024, 7, 30, 9, 57, 28, 890184)),
        ),
    ]
