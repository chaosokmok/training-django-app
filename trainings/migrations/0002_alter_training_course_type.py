# Generated by Django 5.2.4 on 2025-07-09 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='course_type',
            field=models.CharField(choices=[('ด้านสมรรถนะและมาตรฐาน', 'ด้านสมรรถนะและมาตรฐาน'), ('ด้านทักษะดิจิทัล', 'ด้านทักษะดิจิทัล'), ('ด้านการบริหารความเสี่ยง', 'ด้านการบริหารความเสี่ยง')], max_length=50),
        ),
    ]
