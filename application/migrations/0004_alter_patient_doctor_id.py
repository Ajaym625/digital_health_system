# Generated by Django 3.2.7 on 2021-09-07 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_alter_patient_doctor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='doctor_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
