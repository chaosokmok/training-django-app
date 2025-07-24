from django.db import models
from django.contrib.auth.models import User

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
    
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    bio = models.TextField(null=True, blank=True)
    facebook = models.CharField(max_length=100, default="No Facebook")
    tel = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username

