# Generated by Django 3.2.9 on 2021-11-25 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='activate_key',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Ключ активации'),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='activate_key_expired',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
