from django.db import models
from django.contrib.auth.models import User

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    course_number = models.CharField(max_length=20, blank=True)
    section = models.CharField(max_length=50)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes')
    units = models.IntegerField(default=3)
    schedule = models.TextField(blank=True) # Multi-line schedule info

    def __str__(self):
        return f"{self.course_number}: {self.name} - {self.section}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, blank=True)
    section = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')])

    def __str__(self):
        return self.user.username

class PerformanceMonitoring(models.Model):
    PERFORMANCE_TYPES = [
        ('quiz', 'Quiz'),
        ('exam', 'Exam'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('others', 'Others'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performances')
    subject = models.CharField(max_length=100)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)
    performance_type = models.CharField(max_length=20, choices=PERFORMANCE_TYPES, default='others')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.subject} ({self.performance_type})"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')])

    def __str__(self):
        return f"{self.student.username} - {self.classroom.name} - {self.date}"