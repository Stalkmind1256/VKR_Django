from django.db import models
from django.contrib.auth.models import User

# class User(models.Model):
#     username = models.CharField(max_length=100)
#     lastname = models.CharField(max_length=100)
#     middlename = models.CharField(max_length=100)
#     email = models.Email`Field()
#     role = models.CharField(100)
#     date_registr = models.DateTimeField()
class Status(models.Model):
    status_name = models.CharField(max_length=200)

    def __str__(self):
        return self.status_name

class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.category_name


class Suggestion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='suggestions')
    # user_id = models.models.IntegerField(_(""))
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True, related_name='suggestions')
    status = models.ForeignKey(Status,on_delete=models.SET_NULL, null=True, related_name='suggestions')
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


