from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import HRProfile,JobPost,Skill,Experience,JobSkill, UserSkill,ApplicantProfile,JobApplication,Status
from django.db.models import Q
from functools import reduce
# Create your views here.
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render

def applicants(request):
    job_id = request.session.get("job_id")
    jobb = JobPost.objects.get(id = job_id)
    job_applicants = JobApplication.objects.filter(job_post = jobb)
    context = {
        "job_applications": job_applicants
    }

    if request.method == "POST":
        application_id = request.POST.get("application_id")
        new_status_name = request.POST.get('status')
        print(new_status_name)
        # Retrieve the JobApplication object
        application = JobApplication.objects.get(id=application_id)
        
        statuss = Status.objects.get(name=new_status_name)

        application.status = statuss
        application.save()

        # Retrieve the corresponding Status object for the selected status name
        
        # Optionally, add a success message
        messages.success(request, 'Status updated successfully.')

    return render(request, 'applicants.html',context)

def homepage(request):
    return render(request, 'homepage.html')

def hr_dashboard(request):
    job_posts = JobPost.objects.filter(hr=request.user)
    context = {
        "job_posts" : job_posts
    }
    if request.method == "POST":
        job_id = request.POST.get("job_id")
        request.session["job_id"] = job_id
        return redirect('applicants')

    return render(request, 'hr_dashboard.html',context)

def hr_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)

        if user is not None:
           
            login(request,user)

            try:
                ishr = HRProfile.objects.get(user = request.user)
                
            except HRProfile.DoesNotExist:
                messages.error(request,"Forbidden! Not a HR")

            return redirect("hr_dashboard")
        else:
            messages.error(request,"Invalid Credentials")

    return render(request, 'hr_login.html')

def hr_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")

        if password == confirmpassword:
            try:
                password = make_password(password)
                user = User(username = username,password = password,email=email)
                user.save()
                hr = HRProfile(user = user)
                hr.save()
                login(request,user)
                
                return redirect("hr_dashboard")
            except IntegrityError:
                messages.error(request,"Username Already Taken")
        else:
            messages.error("Password confirmation Failed")

    return render(request, 'hr_register.html')

def post_job(request):
    skills = Skill.objects.all()
    experiences = Experience.objects.all()

    context = {
            "skills" : skills,
            "experiences" : experiences
        }
    if request.method == "POST":
        role = request.POST.get("role")
        description = request.POST.get("description")
        skills_required = request.POST.getlist("skills")
        pay = request.POST.get("pay")
        experience = request.POST.get("experience")
        location = request.POST.get("location")
        companyname = request.POST.get("companyname")
        experiencee = Experience.objects.get(experience_value = experience)
        postjob = JobPost(title=role,description=description,pay=pay,location=location,experience_required=experiencee,hr=request.user)
        postjob.save()
        for each_skill in skills_required:
            skilll = Skill.objects.get(name=each_skill)
            jobskill = JobSkill(job_post = postjob, skill = skilll)
            jobskill.save()
            return redirect("hr_dashboard")
    return render(request, 'post_job.html',context)

def user_dashboard(request):
    user = request.user
    
    user_skills = UserSkill.objects.filter(user=request.user).values_list('skill_id', flat=True)

    # Retrieve jobs where at least one required skill matches any of the user's skills
    matching_jobs = JobPost.objects.filter(job_skills__skill_id__in=user_skills).distinct()

    context = {
        "matching_jobs" : matching_jobs
    }

    if request.method == "POST":
        job_id = request.POST.get("job_id")
        job_post = JobPost.objects.get(id=job_id)
        status = Status.objects.get(name="Applied")
        user_id = request.user
        try:
            isapp = JobApplication.objects.get(job_post = job_post, applicant = user_id)
            messages.success(request,"Already Applied")
        except JobApplication.DoesNotExist:
            messages.error(request,"Applied successfully")
            application = JobApplication(job_post =  job_post, applicant = request.user,status=status)
            application.save()
    return render(request, 'user_dashboard.html',context)


def user_details(request):
    skills = Skill.objects.all()
    experiences = Experience.objects.all()

    context = {
        "skills": skills,
        "experiences": experiences
    }
    if request.method == "POST":
        skills_known = request.POST.getlist("skills")
        city = request.POST.get("city")
        contact = request.POST.get("contact")
        experience = request.POST.get("experience")
        experiencee = Experience.objects.get(experience_value = experience)
        user_info = ApplicantProfile(user=request.user, contact_number = contact, location = city, experience = experiencee)
        user_info.save()

        for each_skill_known in skills_known:
            skilll = Skill.objects.get(name = each_skill_known)
            userskill = UserSkill(user = request.user, skill = skilll)
            userskill.save()
            
        return redirect('user_dashboard')


    return render(request, 'user_details.html',context)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("user_dashboard")
        else:
            messages.error(request,"Invalid Credentials")


    return render(request, 'user_login.html')

def user_register(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")

        if password == confirmpassword:
            try:
                password = make_password(password)
                user = User(username = username,password = password,email=email)
                user.save()
                login(request,user)
                return redirect('user_details')
            except IntegrityError:
                messages.error(request,"Username Already Taken")
        else:
            messages.error(request,"Password confirmation Failed")


    return render(request, 'user_register.html')

def view_applicant(request, user_id):
    applicant = User.objects.get(id=user_id)
    user_skills = UserSkill.objects.filter(user=user_id)
    applicant_profile = ApplicantProfile.objects.get(user=user_id)
    context = {
        "applicant" : applicant,
        "user_skills" : user_skills,
        "applicant_profile": applicant_profile
    }
    return render(request, 'view_applicant.html', context)

def applied_jobs(request):
    # Get the current logged-in user
    user = request.user
    
    # Retrieve applied jobs for the current user
    applied_jobs = JobApplication.objects.filter(applicant=user)
    
    return render(request, 'applied_jobs.html', {'applied_jobs': applied_jobs})