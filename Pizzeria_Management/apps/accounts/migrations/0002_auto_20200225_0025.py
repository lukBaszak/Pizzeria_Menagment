# Generated by Django 3.0.3 on 2020-02-25 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Addresses'},
        ),
        migrations.RemoveField(
            model_name='address',
            name='address_name',
        ),
        migrations.AddField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('HM', 'Home'), ('WRK', 'Work'), ('OTHER', 'Other')], max_length=20, null=True),
        ),
    ]
