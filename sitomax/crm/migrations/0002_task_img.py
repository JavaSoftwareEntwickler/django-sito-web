# Generated by Django 5.0.1 on 2024-01-27 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='upload_images/'),
        ),
    ]