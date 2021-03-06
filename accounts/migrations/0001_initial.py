# Generated by Django 2.0.9 on 2019-12-23 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('definition', models.TextField(blank=True)),
                ('logType', models.CharField(choices=[('+', '+'), ('-', '-')], max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccountOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=30)),
                ('lastName', models.CharField(max_length=30)),
                ('phoneNumber', models.CharField(max_length=11)),
                ('nationalCode', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountNumber', models.CharField(max_length=18, unique=True)),
                ('credit', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('O', 'Open'), ('B', 'Blocked'), ('C', 'Closed')], default='O', max_length=1)),
                ('accountOwner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='accounts.AccountOwner')),
            ],
        ),
        migrations.AddField(
            model_name='accountlog',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='accounts.BankAccount'),
        ),
    ]
