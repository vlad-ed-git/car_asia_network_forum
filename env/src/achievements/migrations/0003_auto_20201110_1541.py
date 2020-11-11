# Generated by Django 3.1.2 on 2020-11-10 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0002_auto_20201110_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievementpost',
            name='achievement',
            field=models.CharField(choices=[('RE', 'Reader'), ('DS', 'Discussion Starter'), ('CEL', 'Celebrity'), ('TU', 'Thumbs Up'), ('NM', 'NEW MEMBER')], default='NM', max_length=6),
        ),
    ]
