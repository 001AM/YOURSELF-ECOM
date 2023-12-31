# Generated by Django 2.2.11 on 2023-06-15 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20230615_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('razor_pay_order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razor_pay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razor_pay_payment_signature', models.CharField(blank=True, max_length=100, null=True)),
                ('ord_prod', models.ManyToManyField(to='base.Store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
