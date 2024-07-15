# Generated by Django 5.0.6 on 2024-07-15 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('synopsis', models.TextField()),
                ('author', models.CharField(max_length=50)),
                ('genre', models.CharField(choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Romance', 'Romance'), ('Sci-Fi', 'Sci-Fi'), ('Thriller', 'Thriller'), ('Western', 'Western'), ('Crime', 'Crime')], max_length=10)),
                ('publication_year', models.DateField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('ISBN', models.CharField(editable=False, max_length=10, unique=True)),
            ],
        ),
    ]
