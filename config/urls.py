from django.contrib import admin
from django.urls import path
from portal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('student/', views.student_dash, name='student_dash'),
    path('teacher/', views.teacher_dash, name='teacher_dash'),
    path('classroom/<int:classroom_id>/', views.classroom_detail, name='classroom_detail'),
    path('message/send/', views.send_message, name='send_message'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('grade/add/', views.add_grade, name='add_grade'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/update/', views.profile_update, name='profile_update'),
]