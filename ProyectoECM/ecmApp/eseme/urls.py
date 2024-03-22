from django.urls import path, include

from .views import *

urlpatterns = [
    # ----------------------- SEASONS URL'S -----------------------
    path('season/<int:user_id>', StudentSeasonsAPIView.as_view(), name='student-seasons'),
    path('season/course/<int:user_id>', StudentCoursesAPIView.as_view(), name='student-courses'),
    path('season/list/<int:user>', SeasonListAPIView.as_view(), name='season-list'),
    
    # ----------------------- MEMBERS URL'S -----------------------
    path('members/list', MemberListAPIView.as_view(), name='member-list'),
    
    # ----------------------- COURSES URL'S -----------------------
    path('courses/list', CourseListAPIView.as_view(), name='course-list'),

    # ----------------------- STUDENT URL'S -----------------------
    path('teacher/list/<int:teacher>', TeacherListView.as_view(), name='teacher-list'),
    path('student/update/<int:pk>', StudentUpdateView.as_view(), name='update-student'),
    path('student/list', StudentListAPIView.as_view(), name='student-list'),
    path('student/create', StudentCreateAPIView.as_view(), name='student-create'),
    
    # ----------------------- LOGIN URL'S -----------------------
    path('login/<str:dni>', LoginAPIView.as_view(), name='login'),
]
