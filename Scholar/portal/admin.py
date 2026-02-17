from django.contrib import admin
from .models import Classroom, UserProfile, PerformanceMonitoring, Message, Attendance

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'teacher')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'role')

@admin.register(PerformanceMonitoring)
class PerformanceMonitoringAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'classroom', 'date', 'status')