# Generated by Django 3.1.2 on 2020-12-10 01:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AchievementPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement', models.CharField(choices=[('RE', 'Avid Reader'), ('DS', 'Discussion Starter'), ('CEL', 'Celebrity'), ('TU', 'Thumbs Up'), ('NM', 'NEW MEMBER')], default='NM', max_length=6)),
                ('level', models.PositiveIntegerField(default=1)),
                ('viewed_by_user', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
