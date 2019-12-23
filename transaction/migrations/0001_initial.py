# Generated by Django 2.0.9 on 2019-12-22 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('definition', models.TextField()),
                ('cash', models.BooleanField(default=False)),
                ('fromAccount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactionsFrom', to='accounts.BankAccount')),
                ('toAccount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.BankAccount')),
            ],
        ),
    ]
