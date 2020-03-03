from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
 
LEVEL = (
	("100", 100),
	("200", 200),
	("300", 300),
	("400", 400),
	)

LVL = (
	("300", 300),
	("400", 400),
)

SESSION = (
		("REGULAR", "REGULAR"),
		("WEEKEND", "WEEKEND"),
		("EVENING", "EVENING"),
	)

FACULTY = (
		("INFORMATICS", "INFORMATICS"),
		("ENGINEERING", "ENGINEERING"),
		("BUSINESS", "BUSINESS"),
	)



class CustomUser(AbstractUser):
	is_student = models.BooleanField(default=False)
    

	def __str__(self):
		return self.email

	def get_full_name(self):
		full_name = self.username

		if self.first_name and self.last_name:
			return self.first_name + " " + self.last_name

		else:
			return full_name

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('student_list')


class Student(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	level = models.CharField(choices=LEVEL, max_length=3)
	faculty = models.CharField(choices=FACULTY, max_length=11)
	session = models.CharField(choices=SESSION, max_length=7)
	has_voted = models.BooleanField(default=False)

	def __str__(self):
		return self.user.get_full_name()

	def has_voted_true():
		can = Student.objects.filter(has_voted=True).count()
		return can



class Election(models.Model):
	election_text = models.CharField(max_length=200)
	institution_name = models.CharField(max_length=255)
	slug = models.SlugField()

	def __str__(self):
		return self.election_text

class Position(models.Model):
	text = models.CharField(max_length=80, unique=True)
	election = models.ForeignKey(Election, on_delete=models.CASCADE, default="GETUC")

	def __str__(self):
		return self.text
	
	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('position-list')

class Candidate(models.Model):
	election = models.ForeignKey(Election, on_delete=models.CASCADE, default="N/A")
	position = models.ForeignKey(Position, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	level = models.CharField(choices=LVL, max_length=3)
	faculty = models.CharField(choices=FACULTY, max_length=11)
	picture = models.ImageField(upload_to='candidates/')
	votes = models.IntegerField(default=0, editable=False)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('candidate-list')
	
	
	def vote_count(self):
		total_vote_cast = Student.has_voted_true()
		votes_per_candidate = self.votes

		mul = votes_per_candidate / total_vote_cast
		per = mul * 100
		final_percentage = round(per, 2)
		return final_percentage




			
