# Generated by Django 3.2 on 2021-09-03 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_sum', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('open', 'Открытый'), ('in_progress', 'В обработке'), ('canceled', 'Отмененный'), ('finished', 'Завершенный')], default='open', max_length=20)),
            ],
            options={
                'db_table': 'reserve',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReserveItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='items', to='reserve.reserve')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='reserve_items', to='hotels.hotel')),
            ],
            options={
                'db_table': 'reserve_items',
            },
        ),
        migrations.AddField(
            model_name='reserve',
            name='products',
            field=models.ManyToManyField(through='reserve.ReserveItem', to='hotels.Hotel'),
        ),
        migrations.AddField(
            model_name='reserve',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='reservations', to=settings.AUTH_USER_MODEL),
        ),
    ]
