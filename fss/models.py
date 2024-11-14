from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected')
    ]
    status_name = models.CharField(max_length=200,choices=STATUS_CHOICES)

    def __str__(self):
        return self.status_name

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('technology','Technology'),
        ('education','Education'),
    ]
    category_name = models.CharField(max_length=100,choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.category_name


class Suggestion(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='suggestions')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT, null=True, related_name='suggestions')
    status = models.ForeignKey(Status,on_delete=models.PROTECT, null=True, related_name='suggestions')
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Role(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    role_name = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('user', 'User')], default='user')

    def __str__(self):
        return f"{self.user.username} - {self.role_name}"