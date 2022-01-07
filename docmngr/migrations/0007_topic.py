# Generated by Django 4.0.1 on 2022-01-07 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docmngr', '0006_document_is_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=240)),
                ('documents', models.ManyToManyField(related_name='topics', to='docmngr.Document')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
