# admin.py

from django.contrib import admin
from .models import HRProfile, ApplicantProfile, Skill, UserSkill, JobPost, JobSkill, Status, JobApplication, Experience

# Register your models here.
admin.site.register(HRProfile)
admin.site.register(ApplicantProfile)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(JobPost)
admin.site.register(JobSkill)
admin.site.register(Status)
admin.site.register(JobApplication)
admin.site.register(Experience)
