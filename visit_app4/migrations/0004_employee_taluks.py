# Generated by Django 5.0.1 on 2024-07-23 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit_app4', '0003_remove_dairy_taluk_alter_village_taluk'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='taluks',
            field=models.ManyToManyField(to='visit_app4.taluk'),
        ),
    ]
