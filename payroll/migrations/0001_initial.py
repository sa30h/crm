# Generated by Django 3.0.3 on 2021-07-16 02:53

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
            name='MonthlySalary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_Month', models.DateField(null=True)),
                ('unpaid_leaves', models.PositiveIntegerField(null=True)),
                ('paid_leaves', models.PositiveIntegerField(null=True)),
                ('active_Days', models.PositiveIntegerField()),
                ('working_Days', models.PositiveIntegerField()),
                ('mode_of_payment', models.CharField(choices=[('STRIPE', 'stripe'), ('WORLDPAY', 'worldpay'), ('CHEQUE', 'cheque'), ('BANK_TRANSFER', 'bank_transfer'), ('CASH', 'cash')], max_length=100)),
                ('total_Salary_Amount', models.PositiveIntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'monthlySalary',
            },
        ),
        migrations.CreateModel(
            name='EmployeePackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.IntegerField()),
                ('date_Of_Payment', models.DateField()),
                ('unpaid_leaves_allowed', models.PositiveIntegerField()),
                ('paid_leaves_allowed', models.PositiveIntegerField()),
                ('comments', models.CharField(max_length=100, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'employeeSalary',
            },
        ),
    ]
