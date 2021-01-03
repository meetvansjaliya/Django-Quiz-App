from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


# Create your models here.
class Quiz(models.Model):
	name = models.CharField(max_length=100,default="")
	description = models.CharField(max_length=100)
	pub_date = models.DateField()
	
	class Meta:
		verbose_name = "Quizes"
		
	def __str__(self):
		return self.name

class Question(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	label = models.CharField(max_length=100)
	order = models.IntegerField(default=0)
	option1 = models.CharField(max_length=100, blank=True)
	option2 = models.CharField(max_length=100, blank=True)
	option3 = models.CharField(max_length=100, blank=True)
	option4 = models.CharField(max_length=100, blank=True)
	ans = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.label

	class Meta:
		ordering = ['order']

class QuizTaker(models.Model):
	user_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)	
	score = models.FloatField(default=0)

	def __str__(self):
		return self.user_name.username

	class Meta:
		ordering = ['-score']


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
