# Generated by Django 3.2.7 on 2021-09-07 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_alter_patient_doctor_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='doctor_id',
        ),
    ]