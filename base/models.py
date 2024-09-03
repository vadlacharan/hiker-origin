from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from django.db import models




class HRProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ApplicantProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applicant_profiles')
    
    contact_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    experience = models.ForeignKey('Experience', on_delete=models.CASCADE)


class Skill(models.Model):
    name = models.CharField(max_length=100)


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    


class JobPost(models.Model):
    hr = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    pay = models.IntegerField()
    experience_required = models.ForeignKey('Experience', on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    


class JobSkill(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='job_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)


class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.id


class JobApplication(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='job_applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    


class Experience(models.Model):
    experience_value = models.CharField(max_length=50)
