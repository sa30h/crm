# Generated by Django 3.0.3 on 2021-07-16 02:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=100)),
                ('start_date', models.DateField()),
                ('project_deadline', models.DateField()),
                ('project_status', models.CharField(choices=[('PLANNING', 'Planning'), ('DEVELOPMENT', 'Development'), ('TESTING', 'Testing'), ('DEPLOYMENT', 'Deployment'), ('COMPLETED', 'Completed')], default='', max_length=200, verbose_name='Project stage')),
                ('project_complete_or_Inprogress', models.CharField(choices=[('inprogress', 'INPROGRESS'), ('completed', 'COMPLETED')], max_length=20, verbose_name='Project status')),
                ('estimate_Price_of_Project', models.IntegerField()),
                ('reminder', models.DateField()),
                ('reminder_note', models.TextField(max_length=100)),
                ('business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.Business')),
                ('client_company_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Company')),
                ('responsible_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Project',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_link', to='ProjectManagement.Project')),
                ('project_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('team_lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Employee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_link', to='ProjectManagement.Team')),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_assigned', models.CharField(default='', max_length=100)),
                ('updates', models.CharField(choices=[('allocated', 'Allocated'), ('completed', 'COMPLETED'), ('error', 'ERROR')], max_length=100)),
                ('task_deadline', models.DateField()),
                ('updated_on', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_link', to='ProjectManagement.TeamMember')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_lin', to='ProjectManagement.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Businessopportunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(default='', max_length=100)),
                ('description', models.TextField(max_length=300)),
                ('company_name', models.CharField(max_length=100)),
                ('address', models.CharField(default='', max_length=100)),
                ('contact_person', models.CharField(default='', max_length=100)),
                ('email_id', models.EmailField(default='', max_length=100)),
                ('phone_no', models.CharField(default='', max_length=100)),
                ('additional_contact', models.CharField(default='', max_length=300, null='False')),
                ('details', models.CharField(max_length=300, null='False', verbose_name='')),
                ('start_date', models.DateField()),
                ('deadline', models.DateField()),
                ('followup_date', models.DateField()),
                ('followup_message', models.TextField(default='', max_length=150)),
                ('upload_documents', models.FileField(blank=True, upload_to='')),
                ('responsible_person', models.ManyToManyField(to='authentication.EmployeeProfile')),
            ],
            options={
                'verbose_name_plural': 'Business Opportunity',
            },
        ),
    ]
