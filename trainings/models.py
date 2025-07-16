from django.db import models

class Training(models.Model):
    COURSE_TYPES = [
        ('ด้านสมรรถนะและมาตรฐาน', 'ด้านสมรรถนะและมาตรฐาน'),
        ('ด้านทักษะดิจิทัล', 'ด้านทักษะดิจิทัล'),
        ('ด้านการบริหารความเสี่ยง', 'ด้านการบริหารความเสี่ยง'),
    ]

    course_name = models.CharField(max_length=255)
    course_type = models.CharField(max_length=50, choices=COURSE_TYPES)
    hours = models.PositiveIntegerField()
    date = models.DateField()
    certificate = models.FileField(upload_to='certificates/')

    def __str__(self):
        return f'{self.course_name} ({self.date})'
