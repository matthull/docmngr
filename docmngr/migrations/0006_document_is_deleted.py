# Generated by Django 4.0.1 on 2022-01-07 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docmngr', '0005_document_folder'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
