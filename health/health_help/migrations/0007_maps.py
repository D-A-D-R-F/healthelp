# Generated by Django 3.2.4 on 2021-09-12 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_help', '0006_comments_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map_query', models.CharField(default='', max_length=500)),
                ('doctor_name', models.CharField(default='', max_length=150)),
            ],
        ),
    ]
