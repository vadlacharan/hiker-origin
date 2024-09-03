from django.urls import path
from . import views

urlpatterns = [
    path('applicants/', views.applicants, name='applicants'),
    path('', views.homepage, name='homepage'),
    path('hr/dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('hr/login/', views.hr_login, name='hr_login'),
    path('hr/register/', views.hr_register, name='hr_register'),
    path('hr/post-job/', views.post_job, name='post_job'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/details/', views.user_details, name='user_details'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/register/', views.user_register, name='user_register'),
    path('user/applied-jobs',views.applied_jobs,name="applied_jobs"),
    path('user/<int:user_id>/', views.view_applicant, name='view_applicant'),
]
