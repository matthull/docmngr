# Generated by Django 4.0.1 on 2022-01-06 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docmngr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='parent_folder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='docmngr.folder'),
        ),
    ]
